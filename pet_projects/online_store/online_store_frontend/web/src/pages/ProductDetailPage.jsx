import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";

export default function ProductDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiFetch(`/products/${id}/`)
            .then(res => {
                if (!res.ok) {
                    throw new Error("Product not found");
                }
                return res.json();
            })
            .then(data => setProduct(data))
            .catch(() => setProduct(null))
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

    if (loading) {
        return (
            <div className="product-detail-page">
                <div className="product-detail-card">
                    <strong>Завантаження товару... </strong>
                </div>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="product-detail-page">
                <div className="product-detail-card">
                    Товар не знайдено
                </div>
            </div>
        );
    }

    return (
        <div className="product-detail-card">

            <div className="product-detail-header">
                <h2 className="product-detail-title">{product.title}</h2>

                <div className="product-detail-prices">
                    <strong>
                        Діапазон цін: {product.min_price} – {product.max_price} грн
                    </strong>
                </div>

                {product.max_discount > 0 && (
                    <div className="product-detail-discount">
                        🔥 Максимальна знижка: -{product.max_discount}%
                    </div>
                )}
            </div>

            <hr />

            <div className="product-detail-info">
                <div className="product-detail-row">
                    <span>
                        Категорія: <strong>{product.category?.name}</strong>
                    </span>

                </div>

                {!product.rating_count ? (
                    <div className="seller-no-reviews">Відгуків немає</div>
                ) : (
                    <>
                        <div className="product-detail-rating">
                            Рейтинг: ⭐ {product.rating}/10
                        </div>
                        <div className="product-detail-reviews">
                            Відгуків: {product.rating_count}
                        </div>
                    </>
                )}

                <div className="product-detail-description">
                    <strong>Опис:</strong> {product.description}
                </div>

                {product.quantity === null ? (
                    <div className='product-detail-quantity-null'>
                        В наявності:0
                    </div>
                    ) : (
                        <div className="product-detail-quantity">
                            В наявності: {product.quantity} од. товару
                       </div>
                    )
                }
            </div>

            <div className="product-detail-actions">
                <button
                    className="product-detail-back-btn"
                    onClick={() => navigate(-1)}
                >
                    ← Назад
                </button>
                {isBuyer && (
                    <button
                    className="product-detail-btn-add-review"
                    onClick={() => navigate(`/review/product/create/${product.id}`)}
                    > Залишити відгук про продукт
                </button>
                )}
            </div>
        </div>

    );
}
