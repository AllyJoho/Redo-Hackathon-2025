import React from 'react';

const ScheduleDisplay = ({ schedule, reasoning, majorsConsidered, semester }) => {
  return (
    <div className="schedule-container">
      <h3>📅 Recommended {semester} Schedule</h3>
      <p style={{ marginBottom: '1rem', color: '#666' }}>
        Optimized for: {majorsConsidered.join(', ')}
      </p>
      <ul className="course-list">
        {schedule.map((course, idx) => (
          <li key={idx} className="course-item">
            {course}
          </li>
        ))}
      </ul>
      {reasoning && (
        <div className="reasoning">
          <strong>Why this schedule?</strong><br />
          {reasoning}
        </div>
      )}
    </div>
  );
};

export default ScheduleDisplay;
