import React from 'react';

const MajorCard = ({ major, onClick }) => {
  return (
    <div className="major-card" onClick={() => onClick && onClick(major)}>
      <h3>{major.name}</h3>
      <div className="college">{major.college}</div>
      <div className="description">{major.description}</div>
      <div className="interests">
        {major.interests.slice(0, 5).map((interest, idx) => (
          <span key={idx} className="interest-tag">
            {interest}
          </span>
        ))}
      </div>
      <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
        <div>💼 Avg Salary: ${major.average_salary.toLocaleString()}</div>
        <div>📚 Total Credits: {major.total_credits}</div>
      </div>
    </div>
  );
};

export default MajorCard;
