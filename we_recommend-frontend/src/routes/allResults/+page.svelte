<script>
    import { Button, Card  } from 'attractions';
    import { goto } from '$app/navigation';
    let items = ['', '',]
    let username = 'abc'
    let itemname = 'XX'
</script>

<div class="container">
    <header >
        <h3><a href="/login">Logout</a></h3>
    </header>
    <main>a
        <div class="top_name">
            <h1>Hi {username}</h1>
        </div>

        <div class="management">
            {#each items as item}
                <Card>
                    <span class = "li">{itemname}<Button style="right" href="/">more</Button></span>
                    
                </Card>
            <br>
        
            {/each}

        </div>
    </main>


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
        width: 50%;
        display:inlin-block;
        margin-left:auto;
        margin-right:auto
    }
    .management{
        width: 50%;
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
    .container{
		/* width: 100%; */
		height: 1000px;
		background: linear-gradient(to top, mediumPurple,lavender);	
		/* text-align: center; */
		/* line-height: 400px; */
		/* float: right; */
	}

</style>