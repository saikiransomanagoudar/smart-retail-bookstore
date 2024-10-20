import { SignIn, useUser } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const { isSignedIn } = useUser();
  const navigate = useNavigate();

  if (isSignedIn) {
    navigate("/");
    return null;
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
      <div className="w-full max-w-md">
        <SignIn
          path="/login"
          routing="path"
          signUpUrl="/signup"
          appearance={{
            elements: {
              card: "bg-white shadow-lg rounded-lg text-gray-700 p-6",
              input: "border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 rounded-lg",
              button: "bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg transition-all duration-300",
            },
          }}
        />
      </div>
    </div>
  );
};

export default Login;
