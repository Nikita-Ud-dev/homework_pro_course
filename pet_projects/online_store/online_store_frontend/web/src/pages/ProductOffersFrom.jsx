import {apiFetch} from "../api/client.js";
import {useState, useEffect} from "react";
import {useNavigate, useParams} from "react-router-dom";


export default function ProductSellerForm({ mode = 'create'}) {
    const isEdit = mode === "update";

    const { productId, offerId } = useParams();
    const navigate = useNavigate()

    const [price, setPrice] = useState("");
    const [quantity, setQuantity] = useState("");
    const [discount, setDiscount] = useState(0);
    const [loading, setLoading] = useState(true)

    useEffect(() => {
    if (!isEdit) {
        setLoading(false);
        return;
    }

    apiFetch(`/product-offers/${offerId}/`)
        .then(res => res.json())
        .then(data => {
            setPrice(data.price);
            setQuantity(data.quantity);
            setDiscount(data.discount || 0);
        })
        .finally(() => setLoading(false));
    }, [isEdit, offerId]);


    async function handleSubmit(e) {
        e.preventDefault();
        const url = isEdit
            ? `/product-offers/${offerId}/`
            : `/product-offers/`;

        const method = isEdit ? "PATCH" : "POST";

        const res = await apiFetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                price,
                quantity,
                discount,
                product: productId,
            }),
        });

        setLoading(false);

        if (!res.ok) {
            console.log(await res.json());
            alert('Помилка збереження')
            return;
        }

        navigate(-1);
    }

    return (
        <div className="my-offer-form-page">
            <h2>
                {isEdit ? "✏️ Оновити пропозицію" : "➕ Створити пропозицію"}
            </h2>

            <form onSubmit={handleSubmit} className="my-offer-form">
                <label>Ціна (грн):</label>
                <input
                    type="number"
                    min="1"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    required
                />

                <label>Кількість:</label>
                <input
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    required
                />

                <label>Знижка (%):</label>
                <input
                    type="number"
                    min="0"
                    max="100"
                    value={discount}
                    onChange={(e) => setDiscount(e.target.value)}
                />

                <div className="my-offer-form-actions">
                    <button type="submit" disabled={loading}>
                        {loading
                            ? "Створення..."
                            : isEdit
                                ? "Оновити"
                                : "Створити"}
                    </button>

                    <button
                        type="button"
                        onClick={() => navigate(-1)}
                        className="my-offer-back-btn"
                    >
                        Скасувати
                    </button>
                </div>
            </form>
        </div>
    );
}
