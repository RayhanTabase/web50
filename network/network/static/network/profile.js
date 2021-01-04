
// import Show_posts from "./index"

class Profile extends React.Component{
    constructor(props){
        super(props)
        this.state={
            my_profile:true,
            profile_name:"",
            following:false,
            num_following:"",
            num_followers:"",

        }
    }

    render(){

        return(


        <div> 
            
            <div>
                <div id="profile_name"> Profile name: {this.state.profile_name} </div>
                <div>Followers: {this.state.num_followers} </div>
                <div>Following: {this.state.num_following} </div>
            </div>

            <div style={{marginTop:"10px"}}>
                {!this.state.my_profile ? <button className="btn btn-outline-primary btn-sm" onClick={this.change_follow}> {this.state.following ? "Unfollow":"Follow"} </button>: false }

            </div>
            
        </div>
        )
    }
    componentDidMount(){
        //console.log("set up page")
        this.setup()
       
    }

    setup(){
        // console.log("getting profile")

        Promise.all([fetch(`${window.location}/profile_info`), fetch('/get_user')])

        .then(([user, res2]) => { 
            return Promise.all([user.json(), res2.json()]) 
        })
        .then(([user, res2]) => {
            
            //console.log(user.username,res2.user)
            if(user.username === res2.user){
                //console.log("my profile")

                this.setState({
                    my_profile:true
                })
            }else{
                //console.log("not my profile")
                this.setState({
                    my_profile:false
                })
            }

            if(user.followers.includes(res2.user)){
                //console.log("i am following this")

                this.setState({
                    following:true
                })
            }else{
                // console.log("not following")
            }
            // console.log(user.following,res2)
            //console.log(res1,res2.user)
            this.setState({            
                profile_name:user.username,
                num_following:user.following.length,
                num_followers:user.followers.length,
                initial:false
                    
            })
        }); 
    }

    change_follow = ()=>{             

        fetch(`${window.location}/follow`, {
            method: 'PUT',
            body: JSON.stringify({  

            })
        })
        .then((response)=>{
            return response.json()
        })
        .then((response)=>{
            // console.log(response)
            
            this.setState({
                num_followers : response.num_following,
                following : response.is_following

            })
        })
    }
}

ReactDOM.render(<Profile />,document.querySelector('#profile_info'));