<script>
	import { TextField } from 'attractions';
    import { Button, Modal, Dialog, Loading } from 'attractions';
    import { onMount } from 'svelte';

    import { fetchToken, setToken, setUsername, fetchUsername, removeToken } from "../api/auth"
    import axios from 'axios';
	import { goto } from '$app/navigation';

    let count = 1;
    let list = [""];
    let url = ["","","","","",""];
    let isLoading = false;
    let modalStatus = false;

    let modalOpen = false;
    let isToken = false;
    let passwordi="";
    /**
	 * @type {string | null}
	 */
    let username;

    

    onMount(async () => {

        
        let token = fetchToken();
        console.log("token",token);
        if (token) {
            console.log("sssssssss");
            isToken = true;
            username = fetchUsername();
        } 
        
        console.log("111");


        //console.log(products);
    });

    // function toCompare2() {
    //     toCompare().then(
    //         function (/** @type {any} */ reviews_json) {
    //             reviews_json;
    //         }
    //     );

    async function toCompare() {

        isLoading = true;
        var re = /dp\/B\w{9}\//;
        var s;
        let url_list = [];

        for(let i=0;i<5;i++) {
            if (url[i]){
                s = url[i].match(re);
                console.log(s)
                url_list.push(s[0].slice(3, 13));
            }
            
        }
        console.log(url_list);
        console.log(JSON.stringify(url_list));
        var mydate = new Date();
        var profile = "cms"+mydate.getDay()+ mydate.getHours()+ mydate.getMinutes()+mydate.getSeconds()+mydate.getMilliseconds()+ Math.round(Math.random() * 10000);
            
        /**
		 * @type {any[]}
		 */
        var reviews_json = [];

        for(var j=0;j<url_list.length;j++) {
            await axios.get('http://localhost:8083/api/reviews_all',{
            params:{
                asin: url_list[j]
            }
         })
         .then(function(response){
            console.log(response.data);
            var original_review = response.data
            original_review["profile"] = profile
            original_review["username"] = username
            reviews_json.push(original_review);

        //    if (j==url_list.length-1){
        //     return reviews_json;
        //    }
         })
         .catch(function(error){
           console.log(error,'error');
         });
        }
        // var mmm = {
        //     reviews_detail: reviews_json
        //  }

        await axios.put('http://localhost:8895/reviews',JSON.stringify(reviews_json)).then(function(response){
            //if (response.data.code == '000'){
            if (response.data){
                console.log("aaaaaa")
                console.log(response.data);

                // if (j == url_list.length - 1) {
                //     isLoading = false;
                //     goto("/result/"+profile)
                // }
                isLoading = false;
                goto("/result/"+profile)
            
            } else{
                modalStatus = true;
                console.log('failed');
            }
        }).catch(function(error){
           console.log(error,'error');
         });
        
        //  var mmm = {
        //     reviews_detail: reviews_json
        //  }
        console.log("reviews_json", JSON.stringify(reviews_json))
        
    }



    function logout(){
        removeToken();
        goto('/login')
    }

    async function toTest() {
        await axios.post('http://localhost:8085/api/test',
            {
                li: [1,2,3]
            }
         )
         .then(function(response){
           console.log(response.data);

        //    if (j==url_list.length-1){
        //     return reviews_json;
        //    }
         })
         .catch(function(error){
           console.log(error,'error');
         });
    }

    function handleClick() {
        var re = /dp\/B\w{9}\//;
        var str = "https://www.amazon.com/-/zh/dp/B01H6GUCCQ/ref=sr_1_2?keywords=gaming+headsets&pd_rd_r=26e2d062-5126-4725-b133-351819409b5e&pd_rd_w=WBvzh&pd_rd_wg=ufXQz&pf_rd_p=971294fa-7a1b-4a02-89ed-49f0f15a6df4&pf_rd_r=9N9ED2XJ7HDV9N9D0GDJ&qid=1677541653&sr=8-2"
        var match = str.match(re);
        console.log("sss",match);
        if (count >= 5) {
            modalOpen = true;
        } else {
            count += 1;
            list = [...list,""];
            console.log(list);
        }
        
    }
</script>


<div class="container">
    <!-- <Button filled on:click={logout}>sssss</Button> -->
    <header>
        {#if isToken}
        <h3>{username} | <a href="/allResults">Your Result</a> | <a on:click={logout}>logout</a></h3>
        
        {/if}

        {#if !isToken}
        <h3><a href="/login">Login</a> | <a href="/register">Register</a></h3>
        {/if}
    </header>
    
    <main>
        <div class="top_name">
            <h1>We Recommend!</h1>
        </div>
    

        <div class='textfield'>

            
            <!-- {#each list as value,i}
        
            <TextField outline label="URL {i+1}" bind:value={i} withItem></TextField>
            <br>
        
            {/each} -->
            
            <TextField outline label="URL" bind:value={url[0]} withItem></TextField>
            <br>

            {#if (count===2)}
            <TextField outline label="URL" bind:value={url[1]} withItem></TextField>
            <br>
            {/if}
            
            {#if (count===3)}
            <TextField outline label="URL" bind:value={url[1]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[2]} withItem></TextField>
            <br>
            
            {/if}

            {#if (count===4)}
            <TextField outline label="URL" bind:value={url[1]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[2]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[3]} withItem></TextField>
            <br>
            {/if}

            {#if (count>=5)}
            <TextField outline label="URL" bind:value={url[1]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[2]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[3]} withItem></TextField>
            <br>
            <TextField outline label="URL" bind:value={url[4]} withItem></TextField>
            <br>
            {/if}

            {#if isLoading}
            <Loading />
            {/if}

            <Modal bind:open={modalStatus} let:closeCallback>
                <Dialog title="Warning" {closeCallback}>
                    Analyse Error!
                </Dialog>
            </Modal> 

            <Modal bind:open={modalOpen} let:closeCallback>
                <Dialog title="Warning" {closeCallback}>
                    Maximum number of comparable pairs reached!
                </Dialog>
            </Modal> 



            <!-- <Modal bind:open={modalOpen} let:closeCallback>
                <Dialog title="Warning" {closeCallback}>
                    Please choose properties you want *_*
                </Dialog>
            </Modal> -->
        
            <div class="button">
                <div class="add">
                    <Button round neutral on:click={handleClick}>+</Button>
                </div>
                <br>
            
                <Button filled on:click={toCompare}>Compare Now!</Button>
            </div>

            <!-- <Button filled on:click={toTest}>Compare Now!</Button> -->
            
        </div>
        
    </main>
    
    <footer>
    
    </footer>

</div>



<style>
    
    header{
        height: 150px;
        text-align: right;
        width: 100%;
    }

    .top_name{
        font-family: 'Courier New', Courier, monospace;
        font-size: xx-large;
        width: 30%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto
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

    .li{
        display: flex;
        justify-content: space-between;
    }
</style>

