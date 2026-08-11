import { Droppable, Draggable } from "@hello-pangea/dnd";
import CandidateCard from "./CandidateCard";
import styles from "./Column.module.css";

const STAGE_COLORS = {
  "Applying Period": "#f59e0b",
  "Screening": "#22c55e",
  "Interview": "#ef4444",
  "Test": "#6366f1",
};

const SKELETON_COUNTS = [3, 2, 2, 3];

function SkeletonCard() {
  return (
    <div className={styles.skeletonCard}>
      <div className={styles.skeletonRow}>
        <div className={styles.skeletonAvatar} />
        <div className={styles.skeletonLines}>
          <div className={styles.skeletonLine} />
          <div className={`${styles.skeletonLine} ${styles.skeletonLineShort}`} />
        </div>
      </div>
      <div className={`${styles.skeletonLine} ${styles.skeletonLineBadge}`} />
    </div>
  );
}

function Column({ stage, droppableId, candidates, onCandidateClick, isLoading }) {
  const accentColor = STAGE_COLORS[stage] || "#6b7280";
  const columnIndex = parseInt(droppableId);

  return (
    <div className={styles.column}>
      <div className={styles.header}>
        <span className={styles.stageBadge} style={{ backgroundColor: accentColor }}>
          {stage}
        </span>
        {!isLoading && <span className={styles.count}>{candidates.length}</span>}
        <span className={styles.detailLink}>Detail ›</span>
      </div>

      {isLoading ? (
        <div className={styles.cardList}>
          {Array.from({ length: SKELETON_COUNTS[columnIndex] || 2 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : (
        <Droppable droppableId={droppableId}>
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className={`${styles.cardList} ${snapshot.isDraggingOver ? styles.dragOver : ""}`}
            >
              {candidates.length === 0 ? (
                <div className={styles.emptyState}>
                  No candidates in this stage yet
                </div>
              ) : (
                candidates.map((candidate, index) => (
                  <Draggable
                    key={candidate.id}
                    draggableId={String(candidate.id)}
                    index={index}
                  >
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        <CandidateCard
                          candidate={candidate}
                          isDragging={snapshot.isDragging}
                          onClick={() => onCandidateClick(candidate)}
                        />
                      </div>
                    )}
                  </Draggable>
                ))
              )}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      )}
    </div>
  );
}

export default Column;
