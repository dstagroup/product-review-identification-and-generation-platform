<script>
    import { Divider, Chip, Headline, Tab, Tabs, H2, Slider, StarRating, Dot, Card, Table, Button } from 'attractions';
    import { onMount } from 'svelte';
    import { fetchToken, setToken, setUsername, fetchUsername, removeToken } from "../../../api/auth";
    import axios from 'axios';

    /** @type {import('./$types').PageData} */
    export let data;
    let url = "https://www.baidu.com";
    let restaurantRating = 2;
    

    /**
	 * @type {any[]}
	 */
    let rates = [];
    let recommend_url = "zzzzzz";
    let recommend_rate = 5;
    let recommend_properties = [];
    let list = ["", ""];
    let list_products = [];
    let products = {};
    let selectedTab = 'Details';
    let val = 4.73;
    let image_url = "";
    let src = "images/background.jpg";
    let keys;
    let values;
    let keys1;
    let values1;
    /**
	 * @type {number}
	 */
    let len_products;
    /**
	 * @type {any}
	 */
    let topwords=[];
    /**
	 * @type {any}
	 */
    let entries;
    /**
	 * @type {never[]}
	 */
    let asins = []
    /**
	 * @type {string | null}
	 */
     let username;
    let isToken = false;
    let profile = "";
    let posrating = {}
    let detail = {}
    let list_numbers = [];
    let a="";
    /**
	 * @type {any[]}
	 */
    let listt = []

    /**
	 * @param {number} index
	 */
    async function getDetail(index) {


        console.log(keys[index])
        // await axios.get('http://localhost:8895//get_one_asin?username='+username+'&profile='+profile+'&property='+)
        // .then(function(response){
            
        // })
        // .catch(function(error){

        // });
    }

    onMount(async () => {

        let token = fetchToken();
        console.log("token",token);
        if (token) {
            console.log("sssssssss");
            isToken = true;
            username = fetchUsername();
        } 
        profile = data.post.title;
        console.log(profile);
        await axios.get('http://localhost:8895/get_asins?username='+username+'&profile='+profile)
        .then(function(response){
            console.log(response.data)
            
            asins = response.data
            axios.put('http://localhost:8895/get_analysis_by_profile_userid',{
                profile: profile,
                username: username,
                asins: asins
            })
            .then(function(response){
                list_products = response.data;
                console.log(response.data)

                list_products = JSON.parse(list_products);

                len_products = asins.length;


                console.log("aaa",list_products[1])

                recommend_rate = list_products[0]["all_rating"]
                recommend_url = "https://www.amazon.com/dp/"+ list_products[0]["asin"]
                src = list_products[0]['main_image'];
                posrating = list_products[0]['posrating'];
                keys = Object.keys(posrating)  // ["foo", "batz"]
                console.log(keys)
                values = Object.values(posrating)  // ["bar", "boink"]
                
                for(var i=0;i<keys.length;i++) {
                    listt.push("")
                }

                entries = Object.entries(posrating)  // [["foo", "bar"], ["batz", "boink"]]
                topwords = list_products[0]['topicword'];
                console.log(topwords);
                detail = list_products[0]['detail'];
                keys1 = Object.keys(detail)  // ["foo", "batz"]
                console.log(keys1)
                values1 = Object.values(detail)  // ["bar", "boink"]
                a = list_products[1]["all_rating"];
                console.log("a",a)
                list_numbers = [0,1]
                console.log(len_products)
                if (len_products > 1) {
                    // for (var j = 0; j < len_products;j++){
                    //     list_numbers.push(j);

                    // }
                    // list_numbers = [0,1];
                } 

            })
            .catch(function(error){
                console.log(error,'error');
            });

        }).catch(function(error){
            console.log("ssss");
        });
        // await axios.put('http://localhost:8895/get_analysis_by_profile_userid/'+profile,{
        //     profile: profile,
        //     username: username,
        //     asins: asins
        //  })
        //  .then(function(response){
        //    console.log(response.data.token,'response.data.token')
        //    if(response.data.token){
        //     setToken(response.data.token)
        //     setUsername(username)
        //     axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
        //     //  navigate("/profile");
        //     console.log("sssss");
        //     return goto('/');
        //    }
        //  })
        //  .catch(function(error){
        //    console.log(error,'error');
           
        //  });

        // try{
        //     products = await amazonScraper.products({ keyword: 'Xbox One', number: 50 });
        // } catch (error) {
        //     console.log(error);
        // }

        // const res = await getRateList();
        // rates = res;
        // recommend_url = res[0].url;
        // recommend_rate = res[0].total_rates;
        // recommend_properties = res[0].properties;
        console.log("111");

        //console.log(products);
    });

    const headers = [
        { text: 'Properties', value: 'properties' },
        { text: 'Rates', value: 'rates' },
    ];
    const items = [
        { properties: 'Price', rates: '4.3' },
        { properties: 'Color', rates: '3.7' },
        { properties: 'Transport', rates: '2.9'},
    ];
    
</script>



<div class="main">
    <!-- <h3 class="top"><a href="https://www.baidu.com">Login</a> | <a href="https://www.baidu.com">Register</a></h3> -->
    <div class="top1"></div>
    <div class="top_name">
        <div class="li">
            <div class="title">We<br>Recommend</div>
            
            <!-- <span class = "li"><StarRating name="restaurant" bind:value={recommend_rate} disabled/><Chip outline>Total Rates: 5.0/5.0</Chip></span> -->
            <div class="star"><br><br><br><StarRating bind:value={recommend_rate} disabled/><Chip>Total Rates: {recommend_rate}/10.0</Chip></div>
            
            
        </div>


        {#each list_numbers as i,ind}

        <div class="divs">
            <span><Chip small >{url}</Chip><Chip small >{i} Total rates: {a}</Chip></span>
            
            <Card outline>
                Total Rates:
                <!-- <Chip small >Total rates: </Chip> -->

                <div class="before_slide"></div>
                
                <Slider
                    bind:value={list_products[i]["all_rating"]}
                    min={0}
                    max={10}
                    step={0.01}
                    tooltips="always"
                />

                <Tabs
                    name="menu"
                    items={['Analysis', 'Details']}
                    bind:value={selectedTab}
                />

                {#if selectedTab == 'Analysis'}

                    <Chip outline>

                    Topwords: 
                    {#each list_products[i]['topicword'] as topword }
                        "{topword}"&ensp;&ensp;
                    {/each}
                    </Chip>

                    {#each listt as m,index }
                        <Button on:click={getDetail(index)}>
                            <Dot success class="mr" />{keys[index]}&ensp;&ensp;{values[index]}
                                <!-- <Chip outline></Chip> -->
                        </Button>
                    {/each}
                
                    
                {/if}

                <Button on:click={getDetail(0)}>
                    <Dot success class="mr" />{keys[0]}&ensp;&ensp;{values[0]}
                        <!-- <Chip outline></Chip> -->
                </Button>

                {#if selectedTab == 'Details'}

                {#each listt as m,index }
                    {#if values1[index]!= null}
                        <Button>
                            <Dot success class="mr" />{keys1[index]}:&ensp;&ensp;{values1[index]}
                                <!-- <Chip outline></Chip> -->
                        </Button>
                    {/if}
                {/each}

                
                    
                {/if}

                

                <!-- <Tab value="2222222" name="nav1" disabled>
                    Installation
                </Tab> -->
            </Card>
        </div>

        {/each}

        
        
        
    </div>
</div>

<style>
    .top{
        margin-top: 0px;
    }
    .main{
        height: 3000px;
		background: linear-gradient(to top, mediumPurple,lavender);
        background-size: 100% 100%;
        /* height: 100%; */
        text-align: right;
        width: 100%;
        /* background-color: #C3B1E1; */
    }
    .lll {
        /* width: 60%; */
        display: flex;
    }
    .top1{
        height: 60px;
        font-weight: bold;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: x-large;
    }

    .top_name{
        /* font-family: 'Courier New', Courier, monospace;
        font-size: x-large;
        font-weight: bold; */
        width: 60%;
        text-align: left;
        display:inlin-block; 
        margin-left:auto;
        margin-right:auto
    }
    /* .divs{
        display: flex;
    } */
    .title{
        color: black;
        width: 50%;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 4.5em;
        font-weight: bold;
    }
    .type{
        width: 100%;
        text-align: right;
        color: black;
        font-weight: bold;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: large;

    }
    .star{
        
    }
    .li{
        display: flex;
        justify-content: space-between;
    }
    .before_slide{
        margin-top: 35px;
    }
    
    span { font-size: 2em;}

</style>