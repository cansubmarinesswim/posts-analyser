import * as React from 'react';

import { Helmet } from 'react-helmet-async';
import { filter } from 'lodash';
import { useState } from 'react';

import {
  Card,
  Table,
  Stack,
  Paper,
  Button,
  Popover,
  Checkbox,
  TableRow,
  MenuItem,
  TableBody,
  TableCell,
  Container,
  Typography,
  IconButton,
  TableContainer,
  TablePagination,
  OutlinedInput,
  InputAdornment
} from '@mui/material';

import { styled, alpha } from '@mui/material/styles';

// components
import Label from '../components/label';
import Iconify from '../components/iconify';
import Scrollbar from '../components/scrollbar';

// sections
import { UserListHead, UserListToolbar } from '../sections/@dashboard/user';

// utils
import { createPost, getPosts, removePost } from '../utils/api';

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: 'post', label: 'Post', alignRight: false },
  { id: 'sentiment', label: 'Sentiment', alignRight: false },
  { id: '' }
];

// ----------------------------------------------------------------------

const StyledMultiline = styled(OutlinedInput)(({ theme }) => ({
  width: 640,
  height: 100,
  transition: theme.transitions.create(['box-shadow', 'width'], {
    easing: theme.transitions.easing.easeInOut,
    duration: theme.transitions.duration.shorter,
  }),
  '&.Mui-focused': {
    width: 900,
    boxShadow: theme.customShadows.z8,
  },
  '& fieldset': {
    borderWidth: `1px !important`,
    borderColor: `${alpha(theme.palette.grey[500], 0.32)} !important`,
  },
}));

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function applySortFilter(array, comparator, query) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  if (query) {
    return filter(array, (_user) => _user.text.toLowerCase().indexOf(query.toLowerCase()) !== -1);
  }
  return stabilizedThis.map((el) => el[0]);
}

export default function UserPage() {
  const [postsList, setPostsList] = useState([]);
  const [error, setError] = useState();

  const [newPost, setNewPost] = useState("");

  const [open, setOpen] = useState(null);
  const [openId, setOpenId] = useState(-1);

  const [page, setPage] = useState(0);

  const [order, setOrder] = useState('asc');

  const [selected, setSelected] = useState([]);

  const [orderBy, setOrderBy] = useState('name');

  const [filterName, setFilterName] = useState('');

  const [rowsPerPage, setRowsPerPage] = useState(10);

  const fetchPosts = async () => {
    const res = await getPosts();
    if (res.error) {
      setError(res.error.name);
    }

    let posts = [];
    Object.keys(res).forEach(key => {
      posts.push({
        id: key,
        text: res[key].content,
        sentiment: res[key].classification
      });
    })
    setPostsList(posts);
  };

  React.useEffect(() => {
    fetchPosts();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (! newPost ) {
      return;
    }
    try {
      const posted = await createPost(newPost);

      if (posted.error) {
        setError(posted.error);
      }

      setNewPost('');
      fetchPosts();
    } catch (err) {
      setError(err);
    }
  };

  const handleOpenMenu = (event, id) => {
    setOpen(event.currentTarget);
    setOpenId(id);
  };

  const handleCloseMenu = () => {
    setOpen(null);
    setOpenId(-1);
  };

  const handleNewPost = (event) => {
    setNewPost(event.currentTarget.value);
  }

  const handleDelete = async () => {
    try {
      await removePost(openId);
      fetchPosts();
    } catch (err) {
      setError(err);
    }
    handleCloseMenu();
  }

  const handleDeleteSelected = async () => {
    try {
      selected.forEach((id) => {
        removePost(id);
      });
      await setSelected([]);
      fetchPosts();
    } catch (err) {
      setError(err);
    }
  }

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelecteds = postsList.map((n) => n.id);
      setSelected(newSelecteds);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, id) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected = [];
    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(selected.slice(0, selectedIndex), selected.slice(selectedIndex + 1));
    }
    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setPage(0);
    setRowsPerPage(parseInt(event.target.value, 10));
  };

  const handleFilterByName = (event) => {
    setPage(0);
    setFilterName(event.target.value);
  };

  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - postsList.length) : 0;

  const filteredUsers = applySortFilter(postsList, getComparator(order, orderBy), filterName);

  const isNotFound = !filteredUsers.length && !!filterName;

  return (
    <>
      <Helmet>
        <title> Posts sentiment </title>
      </Helmet>

      <Container>
          <Typography variant="h4" gutterBottom>
            Posts sentiment
          </Typography>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
        
        <StyledMultiline
          value={newPost}
          onChange={handleNewPost}
          placeholder="Add a new post"
          startAdornment={
            <InputAdornment position="start">
              <Iconify icon="eva:edit-2-outline" sx={{ color: 'text.disabled', width: 20, height: 20 }} />
            </InputAdornment>
          }
        />
          <Button variant="contained" startIcon={<Iconify icon="eva:plus-fill" />} onClick={handleSubmit}>
            Submit
          </Button>
        </Stack>

        <Card>
          <UserListToolbar numSelected={selected.length} filterName={filterName} onFilterName={handleFilterByName} onDelete={handleDeleteSelected} />

          <Scrollbar>
            <TableContainer sx={{ minWidth: 800 }}>
              <Table>
                <UserListHead
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  rowCount={postsList.length}
                  numSelected={selected.length}
                  onRequestSort={handleRequestSort}
                  onSelectAllClick={handleSelectAllClick}
                />
                <TableBody>
                  {filteredUsers.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                    const { id, text, sentiment } = row;
                    let color;
                    
                    switch (sentiment) {
                      case 'positive':
                        color = 'success';
                        break;
                      case 'negative':
                        color = 'error';
                        break;
                      case 'neutral':
                        color = 'info';
                        break;
                      default:
                        throw new Error();
                    }
                    
                    const selectedUser = selected.indexOf(id) !== -1;

                    return (
                      <TableRow hover key={id} tabIndex={-1} role="checkbox" selected={selectedUser}>
                        <TableCell padding="checkbox">
                          <Checkbox checked={selectedUser} onChange={(event) => handleClick(event, id)} />
                        </TableCell>

                        <TableCell component="th" scope="row" padding="none">
                          <Stack direction="row" alignItems="left" spacing={2}>
                            <Typography variant="default">
                              {text}
                            </Typography>
                          </Stack>
                        </TableCell>


                        <TableCell align="left">
                        <Label color={color}>{sentiment}</Label>
                        </TableCell>
                        

                        <TableCell align="right">
                          <IconButton size="large" color="inherit" onClick={(event) => handleOpenMenu(event, id)}>
                            <Iconify icon={'eva:more-vertical-fill'} />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                  {emptyRows > 0 && (
                    <TableRow style={{ height: 53 * emptyRows }}>
                      <TableCell colSpan={6} />
                    </TableRow>
                  )}
                </TableBody>

                {isNotFound && (
                  <TableBody>
                    <TableRow>
                      <TableCell align="center" colSpan={6} sx={{ py: 3 }}>
                        <Paper
                          sx={{
                            textAlign: 'center',
                          }}
                        >
                          <Typography variant="h6" paragraph>
                            Not found
                          </Typography>

                          <Typography variant="body2">
                            No results found for &nbsp;
                            <strong>&quot;{filterName}&quot;</strong>.
                            <br /> Try checking for typos or using complete words.
                          </Typography>
                        </Paper>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                )}
              </Table>
            </TableContainer>
          </Scrollbar>

          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={postsList.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Card>
      </Container>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        PaperProps={{
          sx: {
            p: 1,
            width: 140,
            '& .MuiMenuItem-root': {
              px: 1,
              typography: 'body2',
              borderRadius: 0.75,
            },
          },
        }}
      >
        <MenuItem>
          <Iconify icon={'eva:edit-fill'} sx={{ mr: 2 }} />
          Edit
        </MenuItem>

        <MenuItem sx={{ color: 'error.main' }} onClick={handleDelete}>
          <Iconify icon={'eva:trash-2-outline'} sx={{ mr: 2 }} />
          Delete
        </MenuItem>
      </Popover>
    </>
  );
}