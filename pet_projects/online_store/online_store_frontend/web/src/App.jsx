import { Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./pages/Login.jsx";
import Registration from "./pages/Registration.jsx";
import UserProfilePage from "./pages/UserProfilePage.jsx";
import ProductsCatalogPage from "./pages/ProductsCatalogPage.jsx";
import ProductOffersCatalog from "./pages/ProductOffersCatalog.jsx";
import ProductMyOffers from "./pages/ProductMyOffersPage.jsx";
import ProductOffersForm from "./pages/ProductOffersFrom.jsx";
import SellerReviewCreate from "./pages/SellerReviewCreate.jsx"
import ProductReviewCreate from "./pages/ProductReviewCreate.jsx"
import RequireAuth from "./auth/RequireAuth.jsx";
import CartPage from "./pages/CartPage.jsx"
import OrderCheckoutPage from "./pages/OrderCheckoutPage.jsx"
import OrderListPage from './pages/OrderListPage.jsx'
import OrderDetailPage from './pages/OrderDetailPage.jsx'
import ProductDetailPage from './pages/ProductDetailPage.jsx'
import './App.css'
import './index.css'


export default function App() {
    const [catalogMode, setCatalogMode] = useState("all");

    return (
        <>
            <div className="top-bar">
                Online Store
                <div className="catalog-filter">
                    <label htmlFor="catalogMode">Рекомендації:</label>

                    <select
                        id="catalogMode"
                        value={catalogMode}
                        onChange={(e) => setCatalogMode(e.target.value)}
                    >
                        <option value="all">Усі продукти</option>
                        <option value="recommended">Рекомендовані для мене</option>
                    </select>
                </div>
            </div>
            <Routes>
                {/*<Route path="/" element={<RequireAuth><ProductsCatalogPage /></RequireAuth>} />*/}
                <Route path="/profile" element={<RequireAuth><UserProfilePage /></RequireAuth>} />
                <Route path="/products-catalog" element={<RequireAuth><ProductsCatalogPage catalogMode={catalogMode} /></RequireAuth>} />
                <Route path="/product/:id/detail" element={<RequireAuth><ProductDetailPage /></RequireAuth>} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Registration />} />
                <Route path="*" element={<Navigate to="/products-catalog" replace />} />
                <Route path='/offers-catalog/:id' element={<RequireAuth><ProductOffersCatalog /></RequireAuth>} />
                <Route path='/offers/my-offers/:id' element={<RequireAuth><ProductMyOffers /></RequireAuth>} />
                <Route path='/offers/my-offers/:productId/create' element={<RequireAuth><ProductOffersForm mode='create' /></RequireAuth>} />
                <Route path='/offers/my-offers/:productId/update/:offerId' element={<RequireAuth><ProductOffersForm mode='update' /></RequireAuth>} />
                <Route path='/review/seller/create/:sellerId' element={<RequireAuth><SellerReviewCreate /></RequireAuth>} />
                <Route path='/review/product/create/:productId' element={<RequireAuth><ProductReviewCreate /></RequireAuth>} />
                <Route path='/cart' element={<RequireAuth><CartPage /></RequireAuth>} />
                <Route path='/orders/checkout/:id' element={<RequireAuth><OrderCheckoutPage /></RequireAuth>} />
                <Route path='/orders/:id/pay' element={<RequireAuth><OrderCheckoutPage /></RequireAuth>} />
                <Route path='/orders' element={<RequireAuth><OrderListPage /></RequireAuth>} />
                <Route path='/orders/:id/detail' element={<RequireAuth><OrderDetailPage /></RequireAuth>} />
            </Routes>
        </>
    );
}