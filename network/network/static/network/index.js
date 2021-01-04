

class Comment extends React.Component{
    constructor(props){
        super(props)
        this.state={

        }
    
    }
    render(){
        // console.log(this.props.comment)

        return(
            <ul className="comments-list reply-list">
                <li>                                              
                    <div className="comment-box">
                        <div className="comment-head">
                            <h6 className="comment-name">
                                <button  className="btn btn-link profile_get" value={this.props.creator}> {this.props.creator} </button>
                            </h6>
                            <span>{this.props.timestamp}</span>
                            <i className="fa fa-reply"></i>
                            <i className="fa fa-heart"> </i>
                        </div>
                        <div className="comment-content">
                            {this.props.comment}
                        </div>
                    </div>
                </li>
            </ul>
        )

    }
}






class Post extends React.Component{  
    constructor(props){
        super(props)
        this.state ={
            likes: this.props.likes,
            can_edit:this.props.can_edit,
            post:this.props.post,
            old_post: this.props.post,
            liked:this.props.liked,
            comments:false,
            commenting:false,
        }
    }



    render(){

        
        // console.log(this.state.comments)
        // console.log(this.state.commenting)

        if(this.state.comments){
           
            var comments_component = this.state.comments.map(comment=>{  

                    // console.log(post.creator,post.id,post.comment,post.timestamp)

                    return <Comment  
                        key={comment.id}
                        id={comment.id} 
                        creator={comment.creator} 
                        comment={comment.comment}
                        likes={comment.likes.length}
                        timestamp={comment.timestamp}       
                        />                      
                })  
        }

        //console.log(this.state.can_edit)
        // console.log(this.props.editing)

        return(
            
            <div>
                <div>
                    <li>
                        <div className="comment-main-level"> 
                            <div className="comment-box">
                                <div className="comment-head">
                                    <h6 className="comment-name">
                                        <button  className="btn btn-link profile_get" value={this.props.creator}> {this.props.creator} </button>
                                    </h6>
                                    <span>{this.props.timestamp}</span>
                                    
                                </div>

                                <div className="comment-content">
                                    { this.props.editing ? 
                                        <div >
                                            <div >   
                        
                        
                                                <textarea value={this.state.post} onChange={this.change_value}></textarea>
                        
                                            </div>
                                            
                                            <div>
                                                <button className="btn btn-primary" onClick={this.save_post_changes} > Save </button>
                                            </div >     
                                        </div>
                                    
                                        : 
                                        this.state.post 
                                    
                                    }
                                    
                                </div>
                                    
                                <div style={{padding:"10px",backgroundColor:"white",textAlign:"center"}} >
                                    <div >
                                        { !this.props.editing ?

                                                <span name="edit-option" style={{float:"left"}}>

                                                    {this.state.can_edit ? <button style={{textDecoration:"none"}}  className="btn btn-outline-primary btn-sm" onClick={()=>this.props.edit_the_post(this.props.id)}>Edit</button>:false}
                                                </span>   
                                            :
                                            false
                                        }
                                    
                                        <span name="like-section" style={{float:"right"}}>
                                                
                                            <i style={{color:"red"}}> 
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="heart" xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="bi-heart mx-auto b-icon bi" data-v-41be6633=""><g data-v-41be6633="">
                                            {this.state.liked?

                                                <path fillRule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"></path>
                                                :<path fillRule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"></path>

                                            }
                                                </g></svg>
                                            </i>   

                                            <button className="btn btn-outline-primary btn-sm" style={{marginLeft:"8px",textDecoration:"none"}} onClick={this.likeChange}> Likes {this.state.likes} </button>
                                        
                                        </span >
                                    </div>

                                    <div >  
                                               
                                        <button className="btn btn-outline-primary btn-sm" onClick={this.comment_box}> {!this.state.commenting? "Show Comments": "Hide Comments"} </button>                                               
                                             
                                    </div>
                                    
                                </div>    
                            </div>
                        </div>

                        

                        { this.state.commenting ? 
                            
                            <div>
                                { this.props.log_user ?
                                    <div style={{textAlign:"center",width:"60%",height:"40%",marginLeft:"200px",marginTop:"10px"}} >
                                        <div >   
                                            <textarea className="form-control" id="new_comment"></textarea>
                    
                                        </div>
                                        
                                        <div>
                                            <button className="btn btn-primary" onClick={this.add_comment} > Comment </button>
                                        </div > 

                                        
                                    </div>

                                    : false
                                }
                            
                                
                    
                                <div className="sub-comments" style={{marginBottom:"115px"}}>
                                    {comments_component }
                                </div>


                            </div>
                            
                            
                            :
                            false
                        }

                            


                        
                    </li>
                </div>
            </div> 
        )
    
    }
    componentDidMount(){
        // console.log("setting up post")
        this.get_comments()
    } 

    change_value=(event)=>{
        this.setState({            
            post : event.target.value,
        })
    }
    
    save_post_changes=()=>{
        
        
        this.props.edit_the_post(false)

        fetch(`/editPost/${parseInt(this.props.id)}`, {
            method: 'PUT',
            body: JSON.stringify({
                new_post:this.state.post
                      
            })
        })
        .then(response=>{
            if(response.status === 201){
                alert("Your post is invalid, must be atleast 2 characters")
                // console.log(this.state.post)
                // console.log(this.state.old_post)
                this.setState({
                    post : this.state.old_post
                })
            }
        })
    }

    likeChange =()=>{

        fetch(`/likePost/${parseInt(this.props.id)}`, {
            method: 'PUT',
            body: JSON.stringify({
                      
            })
        })
        .then(response =>{           
            return response.json()         
        })
        .then(respose=>{
            // console.log(respose)

            this.setState({            
                likes: respose.likes, 
                liked: respose.liked              
            });
        })
    }

    get_comments=()=>{
        // console.log("get comments")
        fetch("/getComments", {
            method: 'PUT',
            body: JSON.stringify({
                post_id:this.props.id
                      
            })
        })
        .then(response=>{
            return response.json()
        })
        .then(response=>{
            this.setState({
                comments:response
            })
            // console.log(this.state.comments[0])
        })
    }

    add_comment=()=>{
        var comment = document.querySelector("#new_comment")
        // console.log("add comment",comment.value)
        
        
        fetch("/createComment", {
            method: 'POST',
            body: JSON.stringify({
                post_id : this.props.id,
                comment:comment.value,              
            })
        })
        .then(response=>{
            if(response.status === 201){
                alert("Your comment is invalid, must be atleast 2 characters")
            }
            // console.log(response)

            comment.value = ""
            this.get_comments()
        })     
    }

    comment_box=()=>{
        // console.log(this.state.commenting)
        this.setState(prevState=>({
            commenting : !prevState.commenting
        }))
    }
}





class Show_posts extends React.Component{
    constructor(props){
        super(props)
        this.state ={
            
            posts: [],
            log_user:"",
            page_obj:{
                has_next:false,
                has_previous:false,
                num_pages:"",
                number:"",
                next_page_number:"",
                previous_page_number:""

            },
            post_editing:""
            
        }
    }
  
    render(){
        console.log(this.state.posts)
        // console.log(this.state.page_obj)
        //console.log(this.state.log_user)
        if(this.state.posts.length > 0){       
            const all_posts = this.state.posts
            const post_components = all_posts.map(post=>{  

                var can_edit = false
                var liked = false
                var editing = false
                
                if(this.state.log_user === post.creator){
                    var can_edit = true
                }
                if(this.state.post_editing === post.id){
                    editing = true
                }

                // console.log(editing,post.id)
                
                
                post.likes.forEach(element => {
                    // console.log(element)
                        if(this.state.log_user === element){
                            liked = true
                        //   console.log(`${element} liked this`)
                        }

                        
                });
                
                //console.log("user")

                return <Post 
                    key={post.id} 
                    id={post.id} 
                    creator={post.creator} 
                    post={post.post}
                    likes={post.likes.length}
                    timestamp={post.timestamp}
                    can_edit={can_edit} 
                    liked ={liked} 
                    editing = {editing}          
                    edit_the_post = {this.edit_the_post}     
                    log_user = {this.state.log_user}     
                    />                      
            })  
                        
            return(
                <div>
                    <div style={{marginBottom :"100px"}}> 
                        {post_components}
                        
                    </div>

                    <div>
                    <span className="step-links">
                        <ul className="pagination" style={{ justifyContent: 'center',}} >

                            
                            {this.state.page_obj.has_previous ?

                                <React.Fragment>
                                    <button className="page-link"  onClick={this.change_page} value={1} > first</button> 
                                    <button className="page-link"  onClick={this.change_page} value={this.state.page_obj.previous_page_number} >previous</button>
                                </React.Fragment>

                                : <h1></h1> 
                            }
                            
                                <span className="current" style={{marginLeft:"10px",marginRight:"10px",marginTop:"10px"}} >
                                    Page { this.state.page_obj.number}  of  {this.state.page_obj.num_pages}
                                </span>

                            
                                
                            { this.state.page_obj.has_next ? 
                                <React.Fragment> 
                                    <button className="page-link" onClick={this.change_page} value={this.state.page_obj.next_page_number}  >next</button> 
                                    <button className="page-link" onClick={this.change_page} value={this.state.page_obj.num_pages} >last </button>
                                </React.Fragment>

                            : <h1></h1>
                            }
                            

                        </ul>
                    </span>
                    </div>

                </div>
            );

        }else{
            return(<div>NO POSTS</div> )
        }
    }

    change_page = (event) =>{
        // console.log(event.target.value)
        this.set_up(event.target.value)
    }

    componentDidMount(){  
        this.set_up(1)
        
               
    }

    set_up=(page)=>{
    
        var url = `${window.location}`
        var goto = `/getPosts/ALL`
        var page_title = "All Posts"
        //  console.log(url)
        if(url.startsWith("http://127.0.0.1:8000/following")){
            // console.log("following page loading")
            // this.state.page="FOLLOWING"
            var goto = `/getPosts/FOLLOWING`
            page_title = "Following"
            
         }else if(url.startsWith("http://127.0.0.1:8000/profile")){
            // console.log("profiles page loading")
            goto = `${window.location}/profile_posts`
            page_title = "Profile"
            
        }


        {
            // var title = document.querySelector("title")
            // console.log(title)
            // title.innerHTML=page_title

            var page_heading = document.querySelector("#page_heading")

            page_heading.innerHTML = page_title
        }
        
        Promise.all([fetch(goto, {
            method: 'PUT',
            body: JSON.stringify({
              'page_number': page
            })
          
        }), fetch('/get_user')])

        .then(([res1, res2]) => { 
            return Promise.all([res1.json(), res2.json()]) 
        })
        .then(([res1, res2]) => {
            
            // console.log(res1[1][0])
            var all = res1[0] 
            all.forEach(element=>{
                element.editing = "False"
            })  
            // console.log(all)
            this.setState({  

                posts:res1[0],
                log_user: res2.user,
                page_obj:{
                    has_next:             res1[1][0].has_next,
                    has_previous:         res1[1][0].has_previous,
                    num_pages:             res1[1][0].num_pages,
                    number:               res1[1][0].number,
                    next_page_number:      res1[1][0].next_page_number,
                    previous_page_number:  res1[1][0].previous_page_number,
                }
                    
            })
          
        });
    }

    edit_the_post=(id)=>{
        // console.log("edit the post",id)
        this.setState({
            post_editing : id
            
            
        })

    }

}



ReactDOM.render(<Show_posts />,document.querySelector('#posts_view'));


//export default {Show_posts,Post}


  
  






