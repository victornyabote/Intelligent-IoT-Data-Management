import { useState } from 'react'
import './Login.css'

const Login = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    //When submitting on login screen...
   const handleSubmit = async (e) => {
        e.preventDefault()

        console.log('Email: ', email)
        console.log('Password: ', password)
        
        //Fetch user details from DB
        const response = await fetch()


    }

    return (
       <div className="login">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="email">Email</label>
                    <input 
                        id="email" 
                        type="email" 
                        placeholder="johnsmith@gmail.com"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    ></input>
                </div>
                <div>
                    <label htmlFor="password">Password</label>
                    <input 
                        id="password" 
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    ></input>
                </div>
                <button type="submit">Login</button>
            </form>
            <p>No account? Please register here:</p>
            <a href="/register">Register</a>
       </div> 
    )
}

export default Login