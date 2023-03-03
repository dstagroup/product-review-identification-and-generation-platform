<script>
    import { Button, FormField, TextField, Dialog, Modal } from 'attractions';
    import axios from 'axios';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import md5 from 'js-md5';

    import { fetchToken, setToken } from "../../api/auth"

    // const axiosAPI = axios.create({
    //     baseURL : "http://localhost:8895" // it's not recommended to have this info here.
    // });

    export const ssr = false;  

    let username = "";
    let password = "";
    let modalOpen = "";

    onMount(async () => {

        let token = fetchToken();
        console.log("token",token);
        if (token) {
            return goto('/')
        } 
        });

        
    
        const register = ()=> {
        // const response = await axios.post('/login', {
        //     username: username,
        //     password: password
        // }, {withCredentials:true});

        // if (response.status == 200) {
        //     axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;

        //     console.log(response.data.token);

        //     await push('/');
        // }
        var mydate = new Date();
        var uuid = "cms"+mydate.getDay()+ mydate.getHours()+ mydate.getMinutes()+mydate.getSeconds()+mydate.getMilliseconds()+ Math.round(Math.random() * 10000);
        axios.post('http://localhost:8895/register',{
             username: username,
             password: md5(password),
             userid: uuid
         })
         .then(function(response){
            if (response.data.code == "0000") {
                return goto('/login');
            } else {
                username = "";
                password = "";

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

        <Modal bind:open={modalOpen} let:closeCallback>
            <Dialog title="Warning" {closeCallback}>
                Register successfully!<a href="/login">Login in now!</a>
            </Dialog>
        </Modal>


        
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

            <!-- <form>
                <label>Input Username</label>
                <input type='text' bind:value={username}/>

                <label>Input Password</label>
                <input type='text' bind:value={password}/>

                 <Button filled on:click={login}>Login</Button> 
                <button type='button' on:click={login}>Login</button> 
            </form> -->

            <div class="a">
                <Button filled on:click={register}>Register</Button>
                <br>
                Have an account? 
                <a href="/login">Log in now!</a>
            </div>
            
            
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

