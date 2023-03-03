<script>
    import { Button, FormField, TextField } from 'attractions';
    import axios from 'axios';
    
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    import { fetchToken, setToken, setUsername, fetchUsername } from "../../api/auth"

    // const axiosAPI = axios.create({
    //     baseURL : "http://localhost:8895" // it's not recommended to have this info here.
    // });

    export const ssr = false;  

    let username = "";
    let password = "";

    onMount(async () => {

        let token = fetchToken();
        console.log("token",token);
        if (token) {
            return goto('/')
        } 
        });

    function logout(){
        axios.defaults.headers.common['Authorization'] = null;
    }
    
    const login = ()=> {
        
        axios.post('http://localhost:8895/login',{
             username: username,
             password: password
         })
         .then(function(response){
           console.log(response.data.token,'response.data.token')
           if(response.data.token){
            setToken(response.data.token)
            setUsername(username)
            axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
            //  navigate("/profile");
            console.log("sssss");
            return goto('/');
           }
         })
         .catch(function(error){
           console.log(error,'error');
           
         });
        
    }
</script>

<div class="container">
    <header>

    </header>
    
    <main>
        
        <div class='textfield'>
            <div class="top_name">
                <h1>We Recommend!</h1>
            </div>
            <FormField
                name="Username"
                >
                <TextField bind:value={username}/>
            </FormField>
            <FormField 
                name="Password"
                >
                <TextField type="password" bind:value={password}/>
            </FormField>

            <div class="a">
                <Button filled on:click={login}>Login</Button>
                <br>
                Have no account?
                <a href="/register">Register Now!</a>
            </div>
            
            <Button filled on:click={logout}>sssss</Button>
        </div>
        
    </main>
    
    <footer>
    
    </footer>

</div>



<style>
    header{
        height: 180px;
        text-align: right;
        width: 100%;
    }

    .top_name{
        font-family: 'Courier New', Courier, monospace;
        font-size: xx-large;
        /* width: 35%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto */
    }
    .textfield{
        width: 40%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto
    }
    .add{
        width: 35%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto
    }
    .button{
        width: 30%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto
    }

</style>

