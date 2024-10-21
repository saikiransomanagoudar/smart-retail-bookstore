import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useUser, SignOutButton } from "@clerk/clerk-react";

const Navbar = () => {
  const { isSignedIn } = useUser();
  const navigate = useNavigate();
  const [Nav, setNav] = useState("hidden");
  const [showDropdown, setShowDropdown] = useState(false);

  var links = [{ title: "Home", link: "/" }];

  if (isSignedIn) {
    links.push(
      { title: "All Books", link: "/all-books" },
      { title: "Recommended Books", link: "/recommended-books" },
      { title: "Cart", link: "/cart" }
    );
  }

  const handleAllBooksClick = () => {
    if (!isSignedIn) {
      navigate("/login");
    } else {
      navigate("/all-books");
    }
  };

  return (
    <>
      <nav className="relative flex w-full flex-nowrap items-center justify-between bg-zinc-800 py-2 text-white lg:flex-wrap lg:justify-start lg:py-4">
        <div className="flex w-full flex-wrap items-center justify-between px-3">
          <div className="ms-2 w-3/6 lg:w-1/6">
            <Link
              to="/"
              className="flex text-2xl font-semibold items-center justify-center"
            >
              <img
                src="https://cdn-icons-png.flaticon.com/128/10433/10433049.png"
                alt="logo"
                className="h-10 me-4"
              />
              BookStore
            </Link>
          </div>
          <div className="w-1/6 block lg:hidden">
            <button
              className="block border-0 bg-transparent px-2 hover:no-underline hover:shadow-none focus:no-underline focus:shadow-none focus:outline-none focus:ring-0 lg:hidden"
              type="button"
              onClick={() => setNav(Nav === "hidden" ? "block" : "hidden")}
            >
              <span className="[&>svg]:w-7 [&>svg]:stroke-white">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                >
                  <path d="M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z" />
                </svg>
              </span>
            </button>
          </div>
          <div className="5/6 hidden lg:block">
            <div className="flex items-center">
              {links.map((items, i) => (
                <div
                  className="mx-3 hover:text-blue-300 rounded transition-all duration-300 hover:cursor-pointer"
                  key={i}
                >
                  {items.title === "All Books" ? (
                    <div
                      onClick={handleAllBooksClick}
                      className="text-normal hover:cursor-pointer"
                    >
                      {items.title}
                    </div>
                  ) : (
                    <Link to={items.link} className="text-normal">
                      {items.title}
                    </Link>
                  )}
                </div>
              ))}

              {!isSignedIn ? (
                <>
                  <Link
                    to="/signup"
                    className="rounded bg-blue-500 px-3 py-1 mx-3 hover:bg-white hover:text-zinc-900 transition-all duration-300"
                  >
                    Sign up / Sign in
                  </Link>
                </>
              ) : (
                <div className="relative">
                  <img
                    src="https://cdn-icons-png.flaticon.com/128/149/149071.png"
                    alt="profile"
                    className="h-10 w-10 rounded-full cursor-pointer"
                    onClick={() => setShowDropdown(!showDropdown)}
                  />
                  {showDropdown && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Profile
                      </Link>
                      <SignOutButton>
                        <button className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                          Logout
                        </button>
                      </SignOutButton>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>
      <div className={`5/6 ${Nav} lg:hidden bg-zinc-800 text-white px-12`}>
        <div className="flex flex-col items-center">
          {links.map((items, i) => (
            <div
              className="mx-3 hover:text-blue-300 rounded transition-all duration-300 hover:cursor-pointer my-3"
              key={i}
            >
              <Link
                to={`${items.link}`}
                className="text-normal"
                onClick={() => setNav("hidden")}
              >
                {items.title}
              </Link>
            </div>
          ))}
          {!isSignedIn && (
            <>
              <Link
                to="/login"
                className="rounded border border-blue-500 px-3 py-1 mx-3 hover:bg-white hover:text-zinc-900 transition-all duration-300"
              >
                Sign in
              </Link>
              <Link
                to="/signup"
                className="rounded bg-blue-500 px-3 py-1 my-4 md:my-0 mx-3 hover:bg-white hover:text-zinc-900 transition-all duration-300"
              >
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default Navbar;
