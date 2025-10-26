import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DashNav from '../components/dashnavbar';
import '../styles/admin.css';
import wave from '../styles/images/support_images/wave.svg';

export default function Admin() {
    const [username, setUsername] = useState('');
    const [stats, setStats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [members, setMembers] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8080/api/user', { withCredentials: true })
            .then(response => setUsername(response.data.username))
            .catch(error => console.error('Error fetching user:', error));

        axios.get('http://localhost:8080/api/stats', { withCredentials: true })
            .then(response => {
                setStats(response.data.campaigns || []);
            })
            .catch(error => console.error('Error fetching stats:', error));

        axios.get('http://localhost:8080/api/company/users', { withCredentials: true })
            .then((response) => {
                const data = response.data || {};
                setMembers(data.members || []);
            })
            .catch((error) => {
                console.error('Error fetching organization members:', error?.message || error);
            })
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className='admin-body'>
            <nav><DashNav /></nav>
            <div className="admin-container">
                <img src={wave} className="admin-wave" />
                <div className='admin-bucket'>
                    <div className="admin-header">
                        <h1 className="admin-header-text">Welcome, {username}</h1>
                    </div>

                    <div className="admin-upper">
                        <h2 className="admin-section-title">📊 Campaign Statistics</h2>
                        <div className="admin-stats-grid">
                            {stats.map((c) => (
                                <div key={c._id} className="admin-stat-card">
                                    <p className="admin-stat-title">{c.subject}</p>
                                    <p className="admin-stat-detail">Opens: {c.opens || 0}</p>
                                    <p className="admin-stat-detail">Clicks: {c.clicks || 0}</p>
                                    <p className="admin-stat-detail">Sent: {c.sent_count || 0}</p>
                                </div>
                            ))}
                            {stats.length === 0 && (
                                <p className="admin-placeholder">No campaign data yet.</p>
                            )}
                        </div>
                    </div>

                    <div className='admin-company'>
                        <h2 className="admin-section-title">🏢 Company Members</h2>
                        {loading ? (
                            <p className="admin-placeholder">Loading members…</p>
                        ) : (
                            <ul className="admin-member-list">
                                {members.map(m => (
                                    <li key={m.id} className="admin-member-item">
                                        <strong>{m.username}</strong>
                                        <div className="admin-member-email">{m.email ?? '—'}</div>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
