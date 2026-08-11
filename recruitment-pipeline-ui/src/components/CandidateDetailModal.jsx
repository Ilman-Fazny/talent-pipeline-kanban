import styles from "./CandidateDetailModal.module.css";

function CandidateDetailModal({ candidate, onClose }) {
  const formattedDate = new Date(candidate.application_date).toLocaleDateString("en-US", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.title}>{candidate.name}</h2>
          <button className={styles.closeBtn} onClick={onClose}>✕</button>
        </div>

        <div className={styles.body}>
          <div className={styles.field}>
            <span className={styles.label}>Stage</span>
            <span className={styles.value}>{candidate.stage}</span>
          </div>
          <div className={styles.field}>
            <span className={styles.label}>Applied</span>
            <span className={styles.value}>{formattedDate}</span>
          </div>
          <div className={styles.field}>
            <span className={styles.label}>Overall Score</span>
            <span className={styles.value}>
              {candidate.overall_score !== null ? `${candidate.overall_score} / 5` : "Not assessed"}
            </span>
          </div>
          <div className={styles.field}>
            <span className={styles.label}>Referred</span>
            <span className={styles.value}>{candidate.referred ? "Yes" : "No"}</span>
          </div>
          <div className={styles.field}>
            <span className={styles.label}>Assessment</span>
            <span className={styles.value}>{candidate.assessment_status}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CandidateDetailModal;
