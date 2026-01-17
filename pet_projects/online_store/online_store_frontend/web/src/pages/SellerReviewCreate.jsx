import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { apiFetch } from "../api/client.js";

export default function SellerReviewCreate() {
    const {sellerId} = useParams();
    const navigate = useNavigate();

    const [rating, setRating] = useState(0);
    const [comment, setText] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);

        const res = await apiFetch(`/my-seller-reviews/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                seller: sellerId,
                rating,
                comment,
            })
        });

        setLoading(false);

        if (!res.ok) {
            console.log("REVIEW ERROR:", await res.json());
            return;
        }

        navigate(`/products-catalog`);
    }

    return (
        <div className="review-page">
            <h2>Залишити відгук про продавця:</h2>

            <form onSubmit={handleSubmit} className="review-form">
                <label>Оцінка (1-10):</label>
                <input
                    type="number"
                    min="1"
                    max="10"
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                    required
                />

                <label>Ваш відгук:</label>
                <textarea
                    rows="4"
                    value={comment}
                    onChange={(e) => setText(e.target.value)}
                    required
                />

                <button type="submit" disabled={loading}>
                    {loading ? "Надсилання..." : "Надіслати"}
                </button>
            </form>

            <button className='review-button-back-to-offers' onClick={() => navigate(-1)}>Назад</button>
        </div>
    );
}
