import Column from "./Column";
import styles from "./Board.module.css";

function Board({ stages, getCandidatesByStage, onCandidateClick, isLoading, error, onRetry }) {
  if (error) {
    return (
      <div className={styles.board}>
        <div className={styles.errorPanel}>
          <div className={styles.errorIcon}>⚡</div>
          <p className={styles.errorHeading}>Couldn't load candidates</p>
          <p className={styles.errorDetail}>
            Check that the backend is running on port 8000.
          </p>
          <button className={styles.retryBtn} onClick={onRetry}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.board}>
      {stages.map((stage, index) => (
        <Column
          key={stage}
          stage={stage}
          droppableId={String(index)}
          candidates={getCandidatesByStage(stage)}
          onCandidateClick={onCandidateClick}
          isLoading={isLoading}
        />
      ))}
    </div>
  );
}

export default Board;
