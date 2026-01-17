import {apiFetch} from "../api/client.js";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";


export default function ProductsCatalogPage({catalogMode = 'all'}) {

    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        setLoading(true);

        const url =
            catalogMode === "recommended"
            ? "/recommendations"
            : "/products-catalog";

        apiFetch(url)
            .then((res) => res.json())
            .then((data) => {
                setProducts(data);
            })
            .catch((err) => {
                console.log('CATALOG ERROR:', err)
            })
            .finally(() => {
                setLoading(false);
            });
    }, [catalogMode]);

    const [user, setUser] = useState(null);
    const isBuyer = user?.roles?.includes("buyer");
    const isSeller = user?.roles?.includes("seller");

    useEffect(() => {
        apiFetch("/users/me/")
            .then(res => res.json())
            .then(data => setUser(data));
    }, []);


    if (loading) {
        return <h3>Загрузка каталогу...</h3>
    }

    console.log('PRODUCT STATE:', products);
    return (

        <div className='catalog-page'>
            <h2 className={'catalog-title'}>Каталог продуктів</h2>
            <div className="catalog-lines">
                <div className="catalog-line catalog-line-short" />
                <div className="catalog-line catalog-line-long" />
            </div>
            <div className="catalog-grid">
                {products.map((product) => (
                    <div key={product.id} className="product-card">

                        <div className="product-image-box">
                            <img
                                src={product.image_url || "https://via.placeholder.com/200"}
                                alt={product.title}
                                className="product-image"
                            />
                        </div>


                        <h3 className="product-title">{product.title}</h3>

                        {product.category && (
                            <p className="product-category">Категорія: {product.category.name}</p>
                        )}

                        <p className="product-rating">
                            {product.rating ? `Рейтинг: ⭐${product.rating}/10` : "Рейтинг: Немає оцінок ⭐"}
                        </p>
                        {/*{!product.quantity ? (*/}
                        {/*    <p className='product-quantity'>*/}
                        {/*        Немає продуктів на платформі*/}
                        {/*    </p>*/}
                        {/*) :*/}
                        {/*    <p className='product-quantity'>*/}
                        {/*        Кількість продуктів: {product.quantity}*/}
                        {/*    </p>*/}
                        {/*}*/}
                        {product.min_price === product.max_price ? (
                            <p className="product-price">
                                {product.min_price ? `Ціни: Від ${product.min_price} грн` : "Немає пропозицій"}
                            </p>
                        ) : null}

                        {product.min_price < product.max_price ? (
                            <p className="product-price">
                                {product.min_price ? `Ціни: Від ${product.min_price} ` : "Немає пропозицій"}
                                {product.max_price ? `до ${product.max_price} грн` : ""}
                            </p>
                        ) : null}

                        { product.max_discount ? (
                            <p className='product-max-discount'>
                                {product.max_discount ? `Знижки до ${product.max_discount}%!` : ""}
                            </p>
                        ) : null}

                        <div className='product-buttons'>
                            <button
                                className='product-button-detail'
                                onClick={() => navigate(`/product/${product.id}/detail`)}
                                >Детальніше
                            </button>
                            <button className="product-button-favorite">В обране</button>
                            <button
                                className="product-button-offers-catalog"
                                onClick={() => navigate(`/offers-catalog/${product.id}`)}
                                >
                                Пропозиції продавців
                            </button>
                            {isSeller && (
                                <button
                                    className="product-button-my-offers"
                                    onClick={() => navigate(`/offers/my-offers/${product.id}`)}
                                    >
                                    Мої пропозиції на продаж
                                </button>
                            )}
                        </div>

                    </div>
                ))}
                <div className='floating-container'>
                    {isBuyer && (
                        <div
                            className="floating-btn floating-orders-btn"
                            onClick={() => navigate("/orders")}
                            title="Мої замовлення">🧾
                        </div>
                    )}
                    <div
                        className="floating-btn floating-profile"
                        onClick={() => navigate("/profile")}>👤
                    </div>
                    {isBuyer && (
                        <div
                            className="floating-btn floating-cart"
                            onClick={() => navigate("/cart")}>🛒
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
}