import {getAccessToken} from "./token.js";
import {Navigate} from "react-router-dom";

export default function RequireAuth({ children }) {
    const token = getAccessToken();
    if (!token) return <Navigate to={'/login'} replace />;
    return children;
}
