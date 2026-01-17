import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiFetch } from "../api/client.js";

export default function OrderDetailPage() {
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

    if (loading) {
        return (
            <div className="order-detail-page">
                <div className="order-detail-card">
                    Завантаження чеку...
                </div>
            </div>
        );
    }

    if (!order) {
        return (
            <div className="order-detail-page">
                <div className="order-detail-card">
                    Замовлення не знайдено
                </div>
            </div>
        );
    }

    return (
        <div className="order-detail-page">
            {/*Название магазина   */}
            <div className='order-detail-card'>
                <h2 className='order-detail-title'>🧾 Чек замовлення</h2>

                <div className='order-detail-row'>
                    <span>Номер замовлення:</span>
                    <strong>#{id}</strong>
                </div>

                <div className='order-detail-row'>
                    <span>Статус:</span>
                    <span className='order-detail-status'>
                        {order.status === 'paid' ? 'Оплачено' : null}
                    </span>
                </div>

                <hr />

                <h4 className= 'order-detail-item'>Продукти в замовленні:</h4>

                <hr />

                {order.items.map(item => (
                    <div className='order-detail-items' key={item.id}>
                        <div className="order-detail-item-title">Назва: {item.product_title}</div>
                        <div className="order-detail-item-price">Ціна: {item.price_at_time} грн</div>
                        <div className="order-detail-item-quantity">Кількість: {item.quantity} кіл.</div>
                        <div className="order-detail-item-sum">
                            Сумма: {item.total_price_item} грн
                        </div>
                    </div>
                    ))}

                <hr />

                <div className='order-detail-total-price'>
                    Сумма замовлення: {order.total_price} грн
                </div>

                <hr />

                <button
                    className="order-detail-back-btn"
                    onClick={() => navigate('/orders')}>До списку замовлень
                </button>
            </div>
        </div>
    );
}