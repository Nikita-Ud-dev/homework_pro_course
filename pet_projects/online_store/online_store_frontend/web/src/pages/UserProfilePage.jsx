import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import { useNavigate } from "react-router-dom";

export default function ProfilePage() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        apiFetch("/users/me/")
            .then(res => res.json())
            .then(data => setUser(data))
            .finally(() => setLoading(false));
    }, []);

    async function becomeBuyer() {
        const res = await apiFetch("/users/become-buyer/", {
            method: "POST",
        });

        if (!res.ok) {
            alert("Помилка зміни ролі");
            return;
        }

        const updated = await apiFetch("/users/me/").then(r => r.json());
        setUser(updated);
    }

    async function becomeSeller() {
        const res = await apiFetch("/users/become-seller/", {
            method: "POST",
        });

        if (!res.ok) {
            alert("Помилка зміни ролі");
            return;
        }

        const updated = await apiFetch("/users/me/").then(r => r.json());
        setUser(updated);
    }

    if (loading) return <h3>Завантаження профілю...</h3>;

    if (!user) return <h3>Користувача не знайдено</h3>;

    return (
        <div className="profile-page">
            <h2>👤 Профіль користувача</h2>

            <div className="profile-card">
                <div className="profile-row">
                    <strong>Email:</strong> {user.email}
                </div>

                <div className="profile-row">
                    <strong>Імʼя:</strong> {user.full_name || "—"}
                </div>

                <div className="profile-row">
                    <strong>Телефон:</strong> {user.phone_number || "—"}
                </div>

                <div className="profile-row">
                    <strong>Ролі:</strong>
                    <ul className="profile-roles">
                        {user.roles.map(role => (
                            <li key={role}>{role}</li>
                        ))}
                    </ul>
                </div>
                <div className='profile-roles-action-btn'>
                    {!user.roles.includes('buyer') ? (
                        <button
                        className="profile-btn"
                        onClick={becomeBuyer}
                    >
                        ➕ Стати покупцем
                    </button>
                    ) : (
                        <button
                            className="profile-btn"
                            onClick={becomeSeller}
                        >
                            ➕ Стати продавцем
                        </button>
                        )
                    }

                </div>

                <button
                    className="profile-back-btn"
                    onClick={() => navigate(-1)}
                >
                    ← Назад
                </button>
            </div>
        </div>
    );
}

