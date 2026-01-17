import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiFetch } from "../api/client.js";

export default function CheckoutPage() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [order, setOrder] = useState(null)
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiFetch(`/orders/${id}/`)
            .then(res => res.json())
            .then(data => setOrder(data))
            .finally(() => setLoading(false))
    }, [id]);

    async function payOrder(orderId) {
        try {
            setLoading(true);

            const res = await apiFetch(`/orders/${orderId}/pay/`, {
                method: "POST",
            });

            if (!res.ok) {
                throw new Error("Помилка оплати");
            }

            alert("Дякуємо за покупку ❤️");
            navigate("/products-catalog");

        } catch (e) {
            alert("Не вдалося оплатити замовлення");
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return (
            <div className="checkout-page">
                <div className="checkout-card">
                    Завантаження чеку...
                </div>
            </div>
        );
    }

    if (!order) {
        return (
            <div className="checkout-page">
                <div className="checkout-card">
                    Замовлення не знайдено
                </div>
            </div>
        );
    }

    return (
        <div className="checkout-page">
            {/*Название магазина   */}
            <div className='checkout-card'>
                <h2 className='checkout-title'>🧾 Чек замовлення</h2>

                <div className='checkout-row'>
                    <span>Номер замовлення:</span>
                    <strong>#{id}</strong>
                </div>

                <div className='checkout-row'>
                    <span>Статус:</span>
                    <span className='checkout-status'>Очікує оплату</span>
                </div>

                <hr />

                <h4 className= 'checkout-item'>Продукти в замовленні:</h4>

                <hr />

                {order.items.map(item => (
                    <div className='checkout-items' key={item.id}>
                        <div className="checkout-item-title">Назва: {item.product_title}</div>
                        <div className="checkout-item-price">Ціна: {item.price_at_time} грн</div>
                        <div className="checkout-item-quantity">Кількість: {item.quantity} кіл.</div>
                        <div className="checkout-item-sum">
                            Сумма: {item.total_price_item} грн
                        </div>
                    </div>
                    ))}

                <hr />

                <div className='checkout-order-total-price'>
                    Сумма замовлення: {order.total_price} грн
                </div>

                <hr />

                <div className="checkout-payment">
                    <p className='checkout-subtitle'>Спосіб оплати:</p>

                    <label className="checkout-radio">
                        <input type="radio" checked readOnly />
                        Банківська картка (заглушка)
                    </label>

                    <button
                        className="checkout-pay-btn"
                        onClick={() => payOrder(id)}
                        disabled={loading}
                    >
                        {loading ? "Оплата..." : "Оплатити"}
                    </button>
                </div>
            </div>
        </div>
    );
}