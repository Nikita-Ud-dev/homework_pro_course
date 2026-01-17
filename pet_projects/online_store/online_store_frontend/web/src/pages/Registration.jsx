import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("buyer");
    const [phone, setPhone] = useState("");
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);

        const res = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                email,
                password,
                phone_number: phone,
                role,
            }),
        });

        const data = await res.json();

        if (!res.ok) {
            setError("Помилка реєстрації");
            return;
        }

        navigate("/login");
    }

    return (
        <div className="auth-page">
            <form className="auth-card" onSubmit={handleSubmit}>
                <h2 className="auth-title">📝 Реєстрація</h2>

                {error && <div className="auth-error">{error}</div>}

                <div className="auth-field">
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                    />
                </div>

                <div className="auth-field">
                    <label>Пароль</label>
                    <input
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        placeholder='your_password'
                        required
                    />
                </div>
                <div className="auth-field">
                    <label>Телефон</label>
                    <input
                        value={phone}
                        onChange={e => setPhone(e.target.value)}
                        placeholder="+380"
                    />
                </div>

                <div className="auth-field">
                    <label>Оберіть роль</label>
                    <select value={role} onChange={e => setRole(e.target.value)}>
                        <option value="buyer">Покупець</option>
                        <option value="seller">Продавець</option>
                    </select>
                </div>

                <button className="auth-btn" type="submit">
                    Зареєструватися
                </button>

                <div className="auth-footer">
                    <span>Вже є акаунт?</span>
                    <button
                        type="button"
                        className="auth-link"
                        onClick={() => navigate("/login")}
                    >
                        Увійти
                    </button>
                </div>
            </form>
        </div>
    );
}
