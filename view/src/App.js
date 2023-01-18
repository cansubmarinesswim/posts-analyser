import Router from './routes';
import ThemeProvider from './theme';
import ScrollToTop from './components/scroll-to-top';
import { StyledChart } from './components/chart';

import { useEffect, useState } from 'react';
import jwt_decode from 'jwt-decode';
import Header from './layouts/dashboard/header';

import { styled } from '@mui/material/styles';

const APP_BAR_MOBILE = 64;
const APP_BAR_DESKTOP = 92;

const StyledRoot = styled('div')({
  display: 'flex',
  minHeight: '100%',
  overflow: 'hidden',
});

const Main = styled('div')(({ theme }) => ({
  flexGrow: 1,
  overflow: 'auto',
  minHeight: '100%',
  paddingTop: APP_BAR_MOBILE + 24,
  paddingBottom: theme.spacing(10),
  [theme.breakpoints.up('lg')]: {
    paddingTop: APP_BAR_DESKTOP + 24,
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(2),
  },
}));


// ----------------------------------------------------------------------

export default function App() {

  const [user, setUser] = useState(null);
  const [open, setOpen] = useState(false);

  function handleCallbackResponse(response) {
    if (response.error) {
      console.log(response.error);
    } else {
      const decoded = jwt_decode(response.credential);
      console.log(decoded);
      setUser(decoded); 
      document.getElementById("signInDiv").hidden = true;
    }
  }

  function handleLogout() {
    setUser(null);
    document.getElementById("signInDiv").hidden = false;
  };

  useEffect(() => {
    /* global google */
    google.accounts.id.initialize({
      client_id: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      callback: handleCallbackResponse
    });

    google.accounts.id.renderButton(
      document.getElementById('signInDiv'),
      { theme: "outline", size: "large" }
    );

    google.accounts.id.prompt();
  }, []);

  return (
    <ThemeProvider>
      { user && <div>
        <StyledRoot>
          <Header account={user} onOpenNav={() => setOpen(true)} handleLogout={handleLogout} />
          <ScrollToTop />
          <StyledChart />
          <Main>
            <Router />
          </Main>
        </StyledRoot>
      </div>
  }
    <div id="signInDiv"></div>
    </ThemeProvider>
  );
}
