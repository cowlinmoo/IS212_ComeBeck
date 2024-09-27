"use server"

import { cookies } from "next/headers"

interface StoreTokenRequest {  
    token: string  
    id: number
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
    
    cookies().set({
        name: "userId",
        value: request.id.toString(),
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
    
    cookies().set({
        name: "userId",
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

export async function getUserId() {
    return cookies().get("userId")?.value
}
