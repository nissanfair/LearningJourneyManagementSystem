console.log("roles.js load!");
const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      roleName : "",
      roleDesc : "",
      roleImg : "",
      roles: "", // Placeholder for now it is to hold all the roles coming from the back end
    };
  },
  methods: {
    del(id) {
      console.log(id); //check that we got the correct id

      //Confirmation prompt for deletion
      Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then((result) => {

        if (result.isConfirmed) {
          //use axios to pass the data over
          url = "http://localhost:5000/role/" + id + "/softdelete";
          axios
            .get(url)
            .then((response) => {
              // process response.data object
              console.log(response.data.code);
              stat = response.data.code;
              if (stat) {
                Swal.fire("Deleted!", "Role has been deleted.", "success");
              } 
              else {
                Swal.fire({
                  icon: "error",
                  title: "Oops...",
                  text: "Something went wrong!",
                });
              }
            })
            .catch((error) => {
              // process error object
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Something went wrong!",
              });
            });
        }
      });
    },
    create(){
      console.log(this.roleName)
      console.log(this.roleDesc)
      url="http://localhost:5000/role"
      axios.post(url, {
        roleName : this.roleName,
        roleDesc : this.roleDesc
        })
        .then(response => {
        // process response.data
        console.log(response.status)
        console.log(data)
        })
        .catch(error => {
        // process error object
        console.log(error)
        });
    }
  },
  created() {
    url = "http://localhost:5000/role";
    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data.data.roles);
        this.roles = response.data.data.roles;
      })
      .catch((error) => {
        // process error object
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
