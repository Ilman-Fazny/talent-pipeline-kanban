import styles from "./CandidateCard.module.css";

function getInitialColor(name) {
  const colors = ["#f59e0b", "#ef4444", "#22c55e", "#6366f1", "#ec4899", "#14b8a6", "#f97316"];
  let hash = 0;
  for (const char of name) hash = char.charCodeAt(0) + ((hash << 5) - hash);
  return colors[Math.abs(hash) % colors.length];
}

function CandidateCard({ candidate, isDragging, onClick }) {
  const initial = candidate.name.charAt(0).toUpperCase();
  const avatarColor = getInitialColor(candidate.name);

  const formattedDate = new Date(candidate.application_date).toLocaleDateString("en-US", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  return (
    <div
      className={`${styles.card} ${isDragging ? styles.dragging : ""}`}
      onClick={onClick}
    >
      <div className={styles.top}>
        <div className={styles.avatar} style={{ backgroundColor: avatarColor }}>
          {initial}
        </div>
        <div className={styles.info}>
          <span className={styles.name}>{candidate.name}</span>
          <span className={styles.date}>Applied at {formattedDate}</span>
        </div>
        <button className={styles.menuBtn}>⋯</button>
      </div>

      <div className={styles.bottom}>
        {candidate.overall_score !== null ? (
          <span className={styles.score}>
            ★ {candidate.overall_score} Overall
          </span>
        ) : (
          <span className={styles.addAssessment}>+ Add Assessment</span>
        )}

        {candidate.referred && (
          <span className={styles.referredBadge}>& Referred</span>
        )}
      </div>
    </div>
  );
}

export default CandidateCard;
