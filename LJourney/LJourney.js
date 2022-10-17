console.log("LJourney.js load!");
var skill_name = "";
var this_holder = "";//to hold "this" variable in axios, 
//basically a global variable so that the json object can be accessed outside of the axios function scope

const app = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      lj_name: "",
      lj_id: "",
      disabled: false,
      staff_id: "",
      jobrole_id: "", // Placeholder for now it is to hold all the roles coming from the back end
      ljc_id: "",
      course_id: "",
      course_names: []
    };
  },
  methods: {
    del(id) {
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
          url = "http://localhost:5000/jobrole/" + id + "/softdelete";
          axios
            .get(url)
            .then((response) => {
              // process response.data object
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Deleted!",
                  text: "JobRole has been deleted.",
                  icon: "success",
                  allowOutsideClick: false,
                }).then((result) => {
                  if (result.isConfirmed) {
                    //refresh the current page
                    location.reload();
                  }
                });
              } else {
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
    cancel() {
      this.jobrole_name = "";
      this.jobrole_desc = "";
    },
    create() {
      this.disabled = true;

      //Axios post
      url = "http://localhost:5000/jobrole";
      //check if fields are not empty
      if (this.jobrole_name.length == 0 || this.jobrole_desc.length == 0) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "All fields must be filled up!",
        });

        this.disabled = false;
      } else {
        axios
          .post(url, {
            jobrole_name: this.jobrole_name,
            jobrole_desc: this.jobrole_desc,
          })
          .then((response) => {
            // process response.data
            console.log("create response:" + response.data.code);
            stat = response.data.code;
            if (stat) {
              Swal.fire({
                title: "Created!",
                text: "New Job Role has been created.",
                icon: "success",
                allowOutsideClick: false,
  
              }).then((result) => {
                if (result.isConfirmed) {
                  this.disabled = false;
                  //refresh the current page
                  location.reload();
                }
              });
            }
          })
          .catch((error) => {
            // process error object
            this.disabled = false;
            console.log(error.response.status);

            //When jobrole already exists
            if (error.response.status) {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Jobrole already Exists!",
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Oops Something Went Wrong!",
              });
            }
          });
      }
    },
  },
  created() {
    url = "http://localhost:5000/learningjourney";
    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data);
        if (response.data.code == 200) {
          this.lj_name = response.data.data.lj_name;
          this.lj_id = response.data.data.lj_id;

          url2 = "http://localhost:5000/learningjourneycourse/" + lj_id
          axios.get(url2)
          
          .then(r => {
              // here, i expect to get the JSON "array" of course IDs pertaining to this lj_id
              result = r.data;
              for (course in result) {
                  course_url = "http://localhost:5000/course/" + course.course_id
                  axios.get(course_url)
                  .then(res => {
                    this.course_names.push(res.data.course_name)
                  })
              }

          })
         }
            })
      .catch((error) => {
        // process error object
        console.log(error.response.status);
        //When jobroles database is empty
        if (error.response.status == 404) {
          this.message = "<p> There is currently no learning journey created </p>";
        }
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
