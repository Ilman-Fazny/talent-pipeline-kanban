import { useState, useEffect, useCallback } from "react";
import { DragDropContext } from "@hello-pangea/dnd";
import { fetchCandidates, updateCandidateStage } from "./api/candidates";
import Board from "./components/Board";
import CandidateDetailModal from "./components/CandidateDetailModal";
import "./App.css";

const STAGES = ["Applying Period", "Screening", "Interview", "Test"];
const TOAST_DURATION_MS = 3500;

function App() {
  const [candidates, setCandidates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState(null);
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  useEffect(() => {
    loadCandidates();
  }, []);

  async function loadCandidates() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchCandidates();
      setCandidates(data);
    } catch (err) {
      setError(err.message || "Failed to load candidates.");
    } finally {
      setIsLoading(false);
    }
  }

  function getCandidatesByStage(stage) {
    return candidates.filter((c) => c.stage === stage);
  }

  const showToast = useCallback((message) => {
    setToast(message);
    setTimeout(() => setToast(null), TOAST_DURATION_MS);
  }, []);

  async function handleDragEnd(result) {
    const { draggableId, destination } = result;
    if (!destination) return;

    const candidateId = parseInt(draggableId);
    const newStage = STAGES[destination.droppableId];

    const candidate = candidates.find((c) => c.id === candidateId);
    if (!candidate || candidate.stage === newStage) return;

    setCandidates((prev) =>
      prev.map((c) => (c.id === candidateId ? { ...c, stage: newStage } : c))
    );

    try {
      await updateCandidateStage(candidateId, newStage);
    } catch {
      setCandidates((prev) =>
        prev.map((c) =>
          c.id === candidateId ? { ...c, stage: candidate.stage } : c
        )
      );
      showToast("Couldn't update stage, try again");
    }
  }

  return (
    <div className="app">
      <DragDropContext onDragEnd={handleDragEnd}>
        <Board
          stages={STAGES}
          getCandidatesByStage={getCandidatesByStage}
          onCandidateClick={setSelectedCandidate}
          isLoading={isLoading}
          error={error}
          onRetry={loadCandidates}
        />
      </DragDropContext>

      {selectedCandidate && (
        <CandidateDetailModal
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
        />
      )}

      {toast && (
        <div className="toast">
          <span className="toast-icon">⚠</span>
          {toast}
        </div>
      )}
    </div>
  );
}

export default App;
