export const setToken = (token)=>{

    localStorage.setItem('temitope', token)// make up your own token
}

export const setUsername = (username)=>{
    localStorage.setItem('username', username)
}

export const fetchToken = (token)=>{

    return localStorage.getItem('temitope')
}

export const fetchUsername = (username)=>{

    return localStorage.getItem('username')
}

export const removeToken = (token)=>{
    return localStorage.removeItem('temitope')
}