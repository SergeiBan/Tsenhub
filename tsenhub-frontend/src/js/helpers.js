import router from "../router"

export async function refreshAccess() {
    const refreshRequestOptions = {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'refresh': window.localStorage.getItem('refresh')})

    }
    const response = await fetch('api/token/refresh/', refreshRequestOptions)
    if (response['status'] == 401) { 
        window.localStorage.removeItem('access')
        window.localStorage.removeItem('refresh')
        window.localStorage.removeItem('role')
        return 'refresh expired' 
    }

    const responseJSON = await response.json()
    window.localStorage.setItem('access', responseJSON['access'])
    return responseJSON['access']
}
