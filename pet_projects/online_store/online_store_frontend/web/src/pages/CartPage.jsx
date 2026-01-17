import { useEffect, useState, useRef } from "react";
import { apiFetch } from "../api/client.js";
import { useNavigate } from "react-router-dom";

export default function CartPage() {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const timeoutRef = useRef(null);
    const confirmRef = useRef({});
    const [localQty, setLocalQty] = useState({});

    useEffect(() => {
        apiFetch("/cart/")
            .then(res => res.json())
            .then(data => setCart(data))
            .finally(() => setLoading(false));
    }, []);

    function reloadCart() {
        apiFetch("/cart/")
            .then(res => res.json())
            .then(data => setCart(data));
    }

    async function increase(productSellerId) {
        await apiFetch("/cart-items/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                product_seller: productSellerId,
                quantity: 1,
            }),
        });
        setLocalQty(prev => {
            const copy = {...prev};
            delete copy[productSellerId];
            return copy;
        });

        reloadCart();
    }

    async function decrease(cartItemId) {
        await apiFetch(`/cart-items/${cartItemId}/`, {
            method: "DELETE",

        });
        setLocalQty(prev => {
            const copy = {...prev};
            delete copy[cartItemId];
            return copy;
        });

        reloadCart();
    }

    function changeQuantity(cartItemId, value) {
        if (value === undefined) return;

        clearTimeout(timeoutRef.current);

        timeoutRef.current = setTimeout(async () => {
            const quantity = Number(value);
            if (!Number.isInteger(quantity) || quantity < 1) return;

            try {
                const res = await apiFetch(`/cart-items/${cartItemId}/`, {
                    method: "PATCH",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({quantity}),
                });

                if (!res.ok) {
                    throw new Error('bad request')
                }

                reloadCart();

            } catch {
                setLocalQty(prev => {
                    const copy = {...prev};
                    delete copy[cartItemId];
                    return copy;
                });
            }
        }, 500)
    }

    async function createOrder() {
        try {
            const res = await apiFetch("/orders/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
            });

            const data = await res.json();

            navigate(`/orders/checkout/${data.id}`);
        } catch (e) {
            alert("Не вдалося оформити замовлення");
        }
    }

    if (loading) return <h3>Завантаження кошика...</h3>;

    if (!cart || !cart.items || cart.items.length === 0) {
        return (
            <div>
                <h3>Кошик порожній</h3>

                <button className='cart-button-back-to-catalog' onClick={() =>
                    navigate("/products-catalog")}>
                    Продовжити покупки
                </button>
            </div>
        )
    }

    return (
        <div className="cart-page">
            <h2>🛒 Ваш кошик</h2>

            <table className="cart-table">
                <thead>
                <tr>
                    <th>Товар</th>
                    <th>Продавець</th>
                    <th>Ціна</th>
                    <th>Кількість</th>
                    <th>Сума</th>
                </tr>
                </thead>
                <tbody>
                {cart.items.map(item => (
                    <tr key={item.id}>
                        <td className='cart-product-title'>{item.product_title}</td>
                        <td className='cart-seller'>{item.seller}</td>
                        <td>
                            {item.old_price && (
                                <div className="cart-old-price">
                                    <s>{item.old_price} грн</s>
                                    <span className="cart-discount-badge">-{item.discount_percent}%</span>
                                </div>
                            )}
                            <div className="cart-new-price">
                                {item.price} грн
                            </div>
                        </td>
                        <td className="cart-quantity">
                            <button className='qty-btn' onClick={() => increase(item.product_seller, item.id)}>+</button>
                            <button className='qty-btn' onClick={() => decrease(item.id)}>-</button>
                            <input
                                type="number" value={localQty[item.id] ?? item.quantity} min="1"
                                onChange={(e) =>
                                    setLocalQty({...localQty, [item.id]: e.target.value})
                                }
                                onBlur={(e) => {
                                    const confirmButton = confirmRef.current[item.id];

                                    if (!confirmButton || !confirmButton.contains(e.relatedTarget)) {
                                        setLocalQty(prev => {
                                            const copy = {...prev};
                                            delete copy[item.id];
                                            return copy;
                                        });
                                    }
                                }}
                            />
                            <button className='qty-confirm'
                                    ref={el => (confirmRef.current[item.id] = el)}
                                    onClick={() => changeQuantity(item.id, localQty[item.id])}>✔
                            </button>

                        </td>
                        <td className='cart-product-total-price'>{item.total_price_product} грн</td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h3 className='cart-total-price'>Разом: {cart.total_price_cart} грн</h3>
            <button className="cart-order-created-btn"
                    onClick={createOrder}>Оформити замовлення
            </button>

            <button className='cart-button-back-to-catalog' onClick={() => navigate("/products-catalog")}>
                Продовжити покупки
            </button>
        </div>
    );
}