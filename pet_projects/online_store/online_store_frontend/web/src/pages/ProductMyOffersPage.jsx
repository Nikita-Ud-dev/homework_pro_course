import { apiFetch } from "../api/client.js";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import {useNavigate} from "react-router-dom";

export default function ProductOffers() {
    const { id } = useParams();
    const [offers, setOffers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        apiFetch(`/product-offers/?product_id=${id}`)
            .then(res => res.json())
            .then(data => setOffers(data))
            .finally(() => setLoading(false));
    }, [id]);

    if (loading) return <h3>Завантаження пропозицій...</h3>;

    async function handleDeleteOffer(offerId) {
        const confirmDelete = window.confirm("Ви впевнені, що хочете видалити пропозицію?");
        if (!confirmDelete) return;

        const res = await apiFetch(`/product-offers/${offerId}/`, {
            method: "DELETE",
        });

        if (!res.ok) {
            console.log(await res.json());
            alert("Помилка видалення");
            return;
        }

        setOffers(prev => prev.filter(o => o.id !== offerId));
    }

    return (
        <div className="offers-page">
            <h2 className="offers-title" style={{
                    textAlign: "center",
                    marginBottom: "20px",
                    fontSize: "28px",
                    fontWeight: "600",
            }}> 🛒 Мої пропозиції - {offers[0]?.product_title} </h2>
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
                            <th>Дії:</th>
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
                                <td>
                                    <button
                                        className="my-offer-btn-update"
                                        onClick={() => navigate(`/offers/my-offers/${id}/update/${offer.id}`)}
                                    >
                                        Оновити
                                    </button>
                                    <button
                                        className="my-offer-btn-delete"
                                        onClick={() => handleDeleteOffer(offer.id)}
                                    >
                                        Видалити
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
            <button
                className="my-offer-btn-create"
                onClick={() => navigate(`/offers/my-offers/${id}/create`)}
            >
                Створити пропозицію
            </button>
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