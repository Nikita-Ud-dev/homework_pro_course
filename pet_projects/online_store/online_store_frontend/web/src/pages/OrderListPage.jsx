import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import { useNavigate } from "react-router-dom";

export default function OrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        apiFetch("/orders/")
            .then(res => res.json())
            .then(data => setOrders(data))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <h3>Завантаження замовлень...</h3>;

    if (orders.length === 0) {
        return <h3>У вас ще немає замовлень</h3>;
    }

    return (
        <div className="orders-page">
            <h2>📦 Мої замовлення</h2>

            <div className="orders-list">
                {orders.map(order => (
                    <div key={order.id} className="orders-card">
                        <div>
                            <strong>Замовлення #{order.id}</strong>
                        </div>

                        <div>
                            Статус:{" "}
                            <span className={`orders-status ${order.status}`}>
                                {order.status === 'paid' ? 'Оплачено' : 'Очікує оплату'}
                            </span>
                        </div>

                        <div>
                            Сума: <strong>{order.total_price} грн</strong>
                        </div>

                        <div className="orders-actions">
                            {order.status === "created" && (
                                <button
                                    className="orders-pay-btn"
                                    onClick={() => navigate(`/orders/${order.id}/pay`)}
                                >
                                    Оплатити
                                </button>
                            )}

                            {order.status === "paid" && (
                                <button
                                    className="orders-view-btn"
                                    onClick={() => navigate(`/orders/${order.id}/detail`)}
                                >
                                    Переглянути
                                </button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            <button
                className="orders-offer-back-btn"
                onClick={() => navigate(`/products-catalog`)}
            >
                До каталогу
            </button>
        </div>
    );
}
