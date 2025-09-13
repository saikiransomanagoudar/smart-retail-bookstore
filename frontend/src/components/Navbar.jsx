import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUser, SignOutButton } from "@clerk/clerk-react";
import { Search, ShoppingCart, Heart, Menu, X } from "lucide-react";
import { useSelector } from "react-redux";

const SearchBar = ({
  searchQuery,
  handleSearchChange,
  filteredBooks,
  resetSearch,
}) => {
  const navigate = useNavigate();

  const handleResultClick = (book) => {
    resetSearch();
    if (book.id) {
      navigate(`/view-book-details/${book.id}`, { state: { book } });
    } else {
      navigate(`/view-book-details`, { state: { book } });
    }
  };

  return (
    <div className='relative w-full'>
      <input
        type='text'
        placeholder='Search books...'
        value={searchQuery}
        onChange={handleSearchChange}
        className='w-full px-4 py-2 text-gray-900 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
      />
      <Search className='absolute right-3 top-2.5 text-gray-500 w-5 h-5' />

      {/* Enhanced Search Results Dropdown */}
      {filteredBooks.length > 0 && (
        <div className='absolute z-10 mt-2 w-full bg-white rounded-lg shadow-lg max-h-60 overflow-y-auto p-2'>
          {filteredBooks.map((book, index) => (
            <div
              key={index}
              onClick={() => handleResultClick(book)}
              className='flex flex-col items-start p-4 cursor-pointer rounded-lg hover:bg-blue-50 transition duration-150'
            >
              <p className='text-lg font-semibold text-gray-800'>
                {book.title}
              </p>
              {/* {book.author && (
                <p className='text-md text-gray-600'>Author: {book.author}</p>
              )}
              {book.language && (
                <p className='text-sm text-gray-500'>
                  Language: {book.language}
                </p>
              )} */}
              {/* <p className='text-sm text-gray-500'>${book.price.toFixed(2)}</p> */}
              {index < filteredBooks.length - 1 && (
                <hr className='border-t border-gray-200 my-2 w-full' />
              )}
            </div>
          ))}
        </div>
      )}
      {/* Edge case: No results */}
      {searchQuery && filteredBooks.length === 0 && (
        <div className='absolute z-10 mt-2 w-full bg-white rounded-lg shadow-lg p-4 text-gray-500'>
          No books found
        </div>
      )}
    </div>
  );
};

const Navbar = () => {
  const { isSignedIn, user } = useUser();
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredBooks, setFilteredBooks] = useState([]);
  const trendingBooks = useSelector((state) => state.books.trendingBooks);
  const recommendedBooks = useSelector((state) => state.books.recommendedBooks);
  const searchData = [...trendingBooks, ...recommendedBooks];
  const links = [
    { title: "Home", link: "/", icon: null },
    // { title: "Categories", link: "/categories", icon: null },
    // ...(isSignedIn
    //   ? [
    //       {
    //         title: "Cart",
    //         link: "/cart",
    //         icon: <ShoppingCart className='w-5 h-5' />,
    //       },
    //       {
    //         title: "Wishlist",
    //         link: "/wishlist",
    //         icon: <Heart className='w-5 h-5' />,
    //       },
    //     ]
    //   : []),
  ];
  // Function to handle search input
  const handleSearchChange = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);

    if (query.length > 0) {
      const results = searchData.filter((book) =>
        book.title.toLowerCase().includes(query)
      );
      setFilteredBooks(results);
    } else {
      setFilteredBooks([]);
    }
  };

  // Function to reset search state
  const resetSearch = () => {
    setSearchQuery("");
    setFilteredBooks([]);
  };

  return (
    <nav className='fixed w-full top-0 z-50 bg-zinc-900 shadow-lg'>
      {/* Main Navbar */}
      <div className='max-w-7xl mx-auto px-4'>
        <div className='flex items-center justify-between h-16'>
          {/* Logo */}
          <div className='flex-shrink-0'>
            <Link
              to='/'
              className='flex items-center space-x-3'
              onClick={resetSearch}
            >
              <img
                src='https://cdn-icons-png.flaticon.com/128/10433/10433049.png'
                alt='logo'
                className='h-9 w-9'
              />
              <span className='text-white font-bold text-xl'>BookStore</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className='hidden md:flex items-center space-x-8'>
            {/* Search Bar */}
            <div className='w-96'>
              <SearchBar
                searchQuery={searchQuery}
                handleSearchChange={handleSearchChange}
                filteredBooks={filteredBooks}
                resetSearch={resetSearch}
              />
            </div>

            {/* Navigation Links */}
            <div className='flex items-center space-x-6'>
              {links.map((item, i) => (
                <Link
                  key={i}
                  to={item.link}
                  className='flex items-center space-x-1 text-gray-300 hover:text-white transition-colors duration-200'
                  onClick={resetSearch} // Clear search when navigating to a different page
                >
                  {item.icon}
                  <span>{item.title}</span>
                </Link>
              ))}
            </div>

            {/* Auth Section */}
            {!isSignedIn ? (
              <div className='flex items-center'>
                <Link
                  to='/signup'
                  className='bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200'
                  onClick={resetSearch}
                >
                  Join Now
                </Link>
              </div>
            ) : (
              <div className='relative'>
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className='flex items-center space-x-2 focus:outline-none'
                >
                  <img
                    src={
                      user?.imageUrl ||
                      "https://cdn-icons-png.flaticon.com/128/149/149071.png"
                    }
                    alt='profile'
                    className='h-8 w-8 rounded-full border-2 border-blue-500'
                  />
                  <span className='text-gray-300'>{user?.firstName}</span>
                </button>

                {/* Dropdown Menu */}
                {showDropdown && (
                  <div className='absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 z-50'>
                    <div className='px-4 py-2 border-b'>
                      <p className='text-sm font-medium text-gray-900'>
                        {user?.fullName}
                      </p>
                      <p className='text-sm text-gray-500'>
                        {user?.primaryEmailAddress?.emailAddress}
                      </p>
                    </div>
                    <SignOutButton>
                      <button
                        onClick={resetSearch}
                        className='block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100'
                      >
                        Sign out
                      </button>
                    </SignOutButton>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsNavOpen(!isNavOpen)}
            className='md:hidden text-gray-300 hover:text-white'
          >
            {isNavOpen ? (
              <X className='h-6 w-6' />
            ) : (
              <Menu className='h-6 w-6' />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isNavOpen && (
        <div className='md:hidden bg-zinc-900 border-t border-gray-700'>
          <div className='px-4 pt-2 pb-3 space-y-1'>
            {/* Mobile Search Bar */}
            <div className='mb-4'>
              <SearchBar
                searchQuery={searchQuery}
                handleSearchChange={handleSearchChange}
                filteredBooks={filteredBooks}
                resetSearch={resetSearch}
              />
            </div>

            {/* Mobile Navigation Links */}
            {links.map((item, i) => (
              <Link
                key={i}
                to={item.link}
                className='flex items-center space-x-2 px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md transition-colors duration-200'
                onClick={() => {
                  setIsNavOpen(false);
                  resetSearch();
                }}
              >
                {item.icon}
                <span>{item.title}</span>
              </Link>
            ))}

            {/* Mobile Auth Section */}
            {!isSignedIn ? (
              <div className='pt-2 border-t border-gray-700'>
                <Link
                  to='/signup'
                  className='block px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200 text-center'
                  onClick={() => {
                    setIsNavOpen(false);
                    resetSearch();
                  }}
                >
                  Join Now
                </Link>
              </div>
            ) : (
              <div className='space-y-2 pt-2 border-t border-gray-700'>
                <div className='flex items-center space-x-3 px-3 py-2'>
                  <img
                    src={
                      user?.imageUrl ||
                      "https://cdn-icons-png.flaticon.com/128/149/149071.png"
                    }
                    alt='profile'
                    className='h-8 w-8 rounded-full border-2 border-blue-500'
                  />
                  <div>
                    <p className='text-white font-medium'>{user?.firstName}</p>
                    <p className='text-gray-400 text-sm'>
                      {user?.primaryEmailAddress?.emailAddress}
                    </p>
                  </div>
                </div>
                <SignOutButton>
                  <button
                    onClick={() => {
                      setIsNavOpen(false);
                      resetSearch();
                    }}
                    className='block w-full text-left px-3 py-2 text-red-400 hover:text-red-300 hover:bg-gray-800 rounded-md transition-colors duration-200'
                  >
                    Sign out
                  </button>
                </SignOutButton>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
