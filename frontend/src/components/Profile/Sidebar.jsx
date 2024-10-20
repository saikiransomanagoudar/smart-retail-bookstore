import { Link, useNavigate } from "react-router-dom";
import PropTypes from 'prop-types';
import { FaArrowRightFromBracket } from "react-icons/fa6";
import { useUser, SignOutButton } from "@clerk/clerk-react";

const Sidebar = ({ ProfileData }) => {
  const navigate = useNavigate();
  const { user } = useUser();
  const role = user?.publicMetadata?.role || "user";

  return (
    <div className="h-auto lg:h-[100%] flex flex-col p-3 items-center justify-between">
      <div className="flex flex-col items-center w-full">
        <img src={ProfileData.avatar} alt="profile" className="h-[10vh]" />
        <p className="mt-3 text-xl text-zinc-100 font-semibold">
          {ProfileData.username}
        </p>
        <p className="mt-1 text-normal text-zinc-300 ">{ProfileData.email}</p>
        <div className="w-full mt-4 h-[1px] bg-zinc-500 hidden lg:block"></div>
      </div>

      {role !== "admin" && (
        <div className="w-full flex-col items-center justify-center hidden lg:flex">
          <Link
            to="/profile"
            className="text-zinc-100 font-semibold w-full py-2 text-center hover:bg-zinc-900 rounded transition-all duration-300"
          >
            Favourites
          </Link>
          <Link
            to="/profile/orderHistory"
            className="text-zinc-100 font-semibold w-full py-2 mt-4 text-center hover:bg-zinc-900 rounded transition-all duration-300"
          >
            Order History
          </Link>
          <Link
            to="/profile/settings"
            className="text-zinc-100 font-semibold w-full py-2 mt-4 text-center hover:bg-zinc-900 rounded transition-all duration-300"
          >
            Settings
          </Link>
        </div>
      )}

      {role === "admin" && (
        <div className="w-full flex-col items-center justify-center hidden lg:flex">
          <Link
            to="/profile"
            className="text-zinc-100 font-semibold w-full py-2 text-center hover:bg-zinc-900 rounded transition-all duration-300"
          >
            All Orders
          </Link>
          <Link
            to="/profile/add-book"
            className="text-zinc-100 font-semibold w-full py-2 mt-4 text-center hover:bg-zinc-900 rounded transition-all duration-300"
          >
            Add Book
          </Link>
        </div>
      )}

      <SignOutButton>
        <button
          className="bg-zinc-900 w-3/6 lg:w-full mt-4 lg:mt-0 text-white font-semibold flex items-center justify-center py-2 rounded hover:bg-white hover:text-zinc-900 transition-all duration-300"
          onClick={() => {
            navigate("/");
          }}
        >
          Log Out <FaArrowRightFromBracket className="ms-4" />
        </button>
      </SignOutButton>
    </div>
  );
};
Sidebar.propTypes = {
  ProfileData: PropTypes.shape({
    avatar: PropTypes.string.isRequired,
    username: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
  }).isRequired,
};

export default Sidebar;
