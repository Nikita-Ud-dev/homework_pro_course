import { apiFetch } from "../api/client.js";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {useNavigate} from "react-router-dom";

export default function ProductOffersCatalog() {
    const { id } = useParams();
    const [offers, setOffers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        apiFetch(`/product-offers-catalog/?product_id=${id}`)
            .then(res => res.json())
            .then(data => setOffers(data))
            .finally(() => setLoading(false));
    }, [id]);

    const [user, setUser] = useState(null);
    const isBuyer = user?.roles?.includes("buyer");
    const isSeller = user?.roles?.includes("seller");

    useEffect(() => {
        apiFetch("/users/me/")
            .then(res => res.json())
            .then(data => setUser(data));
    }, []);

    if (loading) return <h3>Завантаження пропозицій...</h3>;

    async function handleAddToCart(offerId) {
        const res = await apiFetch("/cart-items/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                product_seller: offerId,
                quantity: 1,
            }),
        });


    if (!res.ok) {
        console.log("ADD TO CART ERROR:", await res.json());
        return;
    }

    alert("Товар додано в кошик 🛒");
    }

    return (
        <div className="offers-page">
            <h2 className="offers-title" style={{
                    textAlign: "center",
                    marginBottom: "20px",
                    fontSize: "28px",
                    fontWeight: "600",
            }}> 🛒 Пропозиції продавців - {offers[0]?.product_title} </h2>
            <h3 style={{
                marginBottom: "15px",
                fontSize: "23px",
                fontWeight: "600",
            }}>Кількість пропозицій: {offers.length}</h3>
            {offers.length === 0 ? (
                <p>Немає пропозицій</p>
            ) : (

                <table className="offers-table">
                    <thead>
                        <tr>
                            <th>Продавець:</th>
                            <th>Рейтинг продавця:</th>
                            <th>Ціна:</th>
                            <th>Знижка:</th>
                            <th>Кількість:</th>
                            <th>Наявніть продукту:</th>
                            <th>Дата:</th>
                            {isBuyer && (
                                <th>Дії:</th>
                            )}
                        </tr>
                    </thead>

                    <tbody>
                        {offers.map(offer => (
                            <tr key={offer.id}>
                                <td>{offer.seller.email}</td>
                                <td className="offer-seller">
                                    <div className="offer-seller-box">
                                        {!offer.seller_rating_count ? (
                                            <div className="seller-no-reviews">Відгуків немає</div>

                                        ) : (
                                            <>
                                                <div className="seller-rating">⭐ {offer.seller_rating}</div>
                                                <div className="seller-reviews">Відгуків: {offer.seller_rating_count}</div>
                                            </>
                                        )}
                                    </div>
                                </td>
                                <td>
                                    {offer.old_price && (
                                        <div className="offer-old-price">
                                            <s>{offer.old_price} грн</s>
                                            <span className="offer-discount-badge">-{offer.discount}%</span>
                                        </div>
                                    )}
                                    <div className="offer-new-price">
                                        {offer.final_price} грн
                                    </div>
                                </td>
                                <td>{offer.discount || 0}%</td>
                                <td>{offer.quantity}</td>
                                <td>
                                    {offer.is_active === true ? (<p>Є в наявності</p>) : <p>Немає в наявності</p>}
                                </td>
                                <td>{offer.created_at.slice(0, 10)}</td>
                                {isBuyer && (
                                    <td>
                                        <button
                                            className="offer-btn-add-to-cart"
                                            onClick={() => handleAddToCart(offer.id)}
                                        >
                                            Додати в корзину
                                        </button>
                                        <button
                                            className="offer-btn-add-review"
                                            onClick={() => navigate(`/review/seller/create/${offer.seller.id}`)}
                                        >
                                            Залишити відгук про продавця
                                        </button>
                                    </td>
                                )}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            <button
                className="offers-back-btn"
                onClick={() => navigate(`/products-catalog`)}
            >
                До каталогу
            </button>
        </div>
    );
}

// <button className='offers-go-back-to-products-catalog' onClick={() => navigate(`/products-catalog`)}>До каталогу продуктів</button>