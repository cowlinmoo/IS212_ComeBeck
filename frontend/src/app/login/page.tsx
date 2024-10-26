"use client";

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from 'next/navigation';
import { storeToken } from '@/lib/cookie';

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const URL = `${BASE_URL}/authenticate`;

export default function LoginPage() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
  
    try {
      const response = await fetch(URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        const jwtToken = data.access_token;
        const userId = data.staff_id;
        await storeToken({ token: jwtToken, id: userId });
        router.push('/overview'); 
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Login failed');
        console.error('Login failed');
      }

    } catch (error) {
      setError('An error occured during login. Please try again.');
      console.error('An error occured during login:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Login</CardTitle>
          <CardDescription className="text-center">
            Enter your username and password to login to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin}>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input 
                  id="username" 
                  type="username" 
                  placeholder="jack.sim@allinone.com.sg"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input 
                  id="password" 
                  type="password" 
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div className="flex items-center space-x-2">
                {error && <p className='text-red-600 text-sm'>{error}</p>}
              </div>
              <Button type="submit" className="w-full" onClick={() => handleLogin}>
                Login
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
