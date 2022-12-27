import { useRoutes } from 'react-router-dom';
import UserPage from './pages/UserPage';

// ----------------------------------------------------------------------

export default function Router() {
  const routes = useRoutes([
    {
      path: '/',
      element: <UserPage />,
    },
  ]);

  return routes;
}