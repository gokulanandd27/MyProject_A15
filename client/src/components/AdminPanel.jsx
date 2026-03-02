
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const AdminPanel = ({ onClose }) => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchUsers = async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const res = await axios.get(`${API_URL}/users`);
            setUsers(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            if (!silent) setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
        const interval = setInterval(() => fetchUsers(true), 1000); // Poll every second for live updates
        return () => clearInterval(interval);
    }, []);

    const handleAction = async (action, username, extraData = {}) => {
        try {
            await axios.post(`${API_URL}/moderate/${action}`, { username, ...extraData });
            fetchUsers(); // Refresh list
        } catch (err) {
            alert(`Failed to ${action} ${username}`);
            console.error(err);
        }
    };

    return (
        <div className="admin-panel-overlay">
            <div className="admin-panel">
                <div className="admin-header">
                    <h2>Admin Dashboard</h2>
                    <button onClick={onClose} className="close-btn">X</button>
                </div>

                <div className="user-list">
                    {users.map(user => (
                        <div key={user.username} className="user-row">
                            <div className="user-info">
                                <span className="username">{user.username}</span>
                                <span className={`status-badge ${user.status}`}>{user.status}</span>
                                <span className="score">Score: {user.reputation_score}</span>
                            </div>
                            <div className="user-actions">
                                {user.status === 'banned' ? (
                                    <button onClick={() => handleAction('unban', user.username)} className="btn-success">Unban</button>
                                ) : (
                                    <button onClick={() => handleAction('ban', user.username)} className="btn-danger">Ban</button>
                                )}

                                {user.status === 'muted' ? (
                                    <button onClick={() => handleAction('unmute', user.username)} className="btn-success">Unmute</button>
                                ) : (
                                    <button onClick={() => handleAction('mute', user.username, { duration: 60 })} className="btn-warning">Mute (1m)</button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default AdminPanel;
