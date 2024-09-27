"use server"  
  
import { cookies } from "next/headers"  
  
interface StoreTokenRequest {  
    token: string  
    // refresh_token: string  
}  
  
export async function storeToken(request: StoreTokenRequest) {  
    cookies().set({  
        name: "accessToken",  
        value: request.token,  
        httpOnly: true,  
        sameSite: "strict",  
        secure: true,
        maxAge: 3600,
    })
}

export async function clearToken() {
    cookies().set({
        name: "accessToken",
        value: "",
        httpOnly: true,
        sameSite: "strict",
        secure: true,
        maxAge: 0,
    })
}

export async function getToken() {
    return cookies().get("accessToken")?.value
}