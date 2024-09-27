import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUserId } from './cookie';

const useAuth = () => {
  const [token, setToken] = useState<string | undefined>(undefined);
  const [userId, setUserId] = useState<string | undefined>(undefined);
  const [pageLoading, setPageLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const fetchToken = async () => {
      const token = await getToken();
      const userId = await getUserId();
      setToken(token);
      setUserId(userId);
      setPageLoading(false);
    };

    fetchToken();
  }, []);

  useEffect(() => {
    if (!token && !pageLoading) {
      router.push('/login');
    }
  }, [token, router, pageLoading]);

  return { token, userId, pageLoading };
};

export default useAuth;
