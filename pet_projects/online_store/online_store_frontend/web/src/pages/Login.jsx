import { setTokens } from "../auth/token.js";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);

    const navigate = useNavigate();

    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);

        const res = await fetch("http://127.0.0.1:8000/api/token/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (!res.ok) {
            setError("Невірний email або пароль");
            return;
        }

        setTokens(data.access, data.refresh);
        navigate("/products-catalog");
    }

    return (
        <div className="auth-page">
            <form className="auth-card" onSubmit={handleSubmit}>
                <h2 className="auth-title">🔐 Вхід</h2>

                {error && <div className="auth-error">{error}</div>}

                <div className="auth-field">
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="example@email.com"
                        required
                    />
                </div>

                <div className="auth-field">
                    <label>Пароль</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="password"
                        required
                    />
                </div>

                <button className="auth-btn" type="submit">
                    Увійти
                </button>

                <div className="auth-footer">
                    <span>Немає акаунта?</span>
                    <button
                        type="button"
                        className="auth-link"
                        onClick={() => navigate("/register")}
                    >
                        Зареєструватися
                    </button>
                </div>
            </form>
        </div>
    );
}
