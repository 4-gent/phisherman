import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/dashboard.css";
import "../styles/loading.css";
import UserNav from "../components/usernavbar";
import wave2 from "../styles/images/support_images/wave2.svg";
import { FaSpinner } from "react-icons/fa";

export default function Dashboard() {
  const [username, setUsername] = useState("");
  const [previousScore, setPreviousScore] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingBoard, setLoadingBoard] = useState(true);

  useEffect(() => {
    // user + previous score
    axios
      .get("http://localhost:8080/api/user", { withCredentials: true })
      .then((res) => {
        const d = res.data || {};
        setUsername(d.username || "");
        setPreviousScore(d.previous_score ?? null);
      })
      .catch((e) => console.error("Error fetching user:", e?.message || e))
      .finally(() => setLoadingUser(false));

    // leaderboard (company-wide)
    axios
      .get("http://localhost:8080/api/all-company", { withCredentials: true })
      .then((res) => {
        const stats = (res.data && res.data.stats) || [];
        const sorted = stats
          .map((s) => ({
            ...s,
            score: typeof s.score === "string" ? Number(s.score) : s.score,
          }))
          .sort((a, b) => (b.score || 0) - (a.score || 0));
        setLeaderboard(sorted);
      })
      .catch((e) =>
        console.error("Error fetching leaderboard:", e?.message || e)
      )
      .finally(() => setLoadingBoard(false));
  }, []);

  return (
    <div className="dashboard-body">
      <nav>
        <UserNav />
      </nav>

      <div className="dashboard-container">
        <img src={wave2} className="dashboard-wave" alt="" />
        <div className='dashboard-bucket'>
        <header className="dashboard-header">
          <h1 className="dashboard-header-text">
            Welcome to your dashboard{username ? `, ${username}` : ""}
          </h1>
        </header>

        <main className="dashboard-content">
          {/* Personal score card */}
          <section className="dashboard-grid">
            <div className="dashboard-card dashboard-card--score">
              <h2 className="dashboard-card-title">Your Previous Score</h2>
              {loadingUser ? (
                <div className="loading-container">
                  <FaSpinner className="loading-icon" />
                </div>
              ) : (
                <p className="dashboard-score-value">
                  {previousScore !== null ? previousScore : "No score yet"}
                </p>
              )}
            </div>

            {/* Leaderboard card */}
            <div className="dashboard-card dashboard-card--leaderboard">
              <h2 className="dashboard-card-title">Company Leaderboard</h2>
              {loadingBoard ? (
                <div className="loading-container">
                  <FaSpinner className="loading-icon" />
                </div>
              ) : leaderboard.length === 0 ? (
                <p className="dashboard-placeholder">No scores yet</p>
              ) : (
                <ol className="dashboard-leaderboard-list">
                  {leaderboard.map((s, idx) => (
                    <li key={s._id ?? idx} className="dashboard-leaderboard-item">
                      <span className={`dashboard-rank badge-${idx + 1}`}>
                        #{idx + 1}
                      </span>
                      <div className="dashboard-leaderboard-info">
                        <strong className="dashboard-username">
                          {s.username ?? s.stats_fk ?? "user"}
                        </strong>
                        <div className="dashboard-leaderboard-score">
                          Score: {s.score ?? 0}
                        </div>
                      </div>
                    </li>
                  ))}
                </ol>
              )}
            </div>
          </section>
        </main>
        </div>
      </div>
    </div>
  );
}
