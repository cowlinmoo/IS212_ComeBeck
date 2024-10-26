import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUserId } from './cookie';
import { Employee, getMyEmployee } from '@/app/schedule/api';

const useAuth = () => {
  const [token, setToken] = useState<string | undefined>(undefined);
  const [userId, setUserId] = useState<string | undefined>(undefined);
  const [user, setUser] = useState<Employee | undefined>(undefined);
  const [pageLoading, setPageLoading] = useState<boolean>(true);

  const router = useRouter();

  useEffect(() => {
    const fetchToken = async () => {
      const token = await getToken();
      const userId = await getUserId();
      const currUser = await getMyEmployee(token as string, Number(userId))
      setUser(currUser)
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

  return { token, userId, pageLoading, user };
};

export default useAuth;
