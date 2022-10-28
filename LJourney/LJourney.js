console.log("LJourney.js load!");

var staff_id = 1;
// get staff_id from url param
try {
  const urlParams = new URLSearchParams(window.location.search);
  staff_id = urlParams.get("staff_id");
  if (staff_id == null) {
    window.location.href = window.location.href + "?staff_id=" + 1;
  }
} catch (error) {
  console.log(error);
}

const app1 = Vue.createApp({
  data() {
    return {
      // name:value pairs here
      // cannot use variables in another variable as you are declaring here
      lj_name: "",
      lj_id: "",
      current_staff_id: "",
      learningjourneys: "",
      staffs: "",
      disabled: false,
      staff_id: "",
      jobrole_id: "", // Placeholder for now it is to hold all the roles coming from the back end
      ljc_id: "",
      course_id: "",
      course_names: [],
      job_roles: [], //This will hold the selection of job roles
      jobroleselection: "", // this will hold the job role selection from the dropdown list
      linked_skills_list: [], //this will hold the skills linked to the selected job role
      courses_list: [], //this will hold the courses that can help clear a particular skill
      selected_skill_id: "", //this will hold the currently selected skill id 
      skill_courses_list : [],
      skill_id:""
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
          url = "http://localhost:5000/learningjourney/" + id;
          axios
            .delete(url)
            .then((response) => {
              // process response.data object
              stat = response.data.code;
              if (stat) {
                Swal.fire({
                  title: "Deleted!",
                  text: "Learning Journey has been deleted.",
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
      this.jobroleselection = "";
      this.linked_skills_list= [];
      this.courses_list = []
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

    //this is called when we click add learning journey
    retrieve() {
      url = "http://localhost:5000/jobrole";
      axios
        .get(url)
        .then((response) => {
          // handle success
          console.log(response.data.data.jobroles);
          this.job_roles = response.data.data.jobroles;
          console.log(this.job_roles);
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        });
    },
    obtain() {
      //here we will try and populate the skills needed for the selected job role
      if (this.jobroleselection != "") {
        url = "http://localhost:5000/jobrole/" + this.jobroleselection;
        axios
          .get(url)
          .then((response) => {
            // handle success
            console.log(response.data.data);
            console.log(response.data.data.linked_skills);
            this.linked_skills_list = response.data.data.linked_skills;
          })
          .catch(function (error) {
            // handle error
            console.log(error);
          });
      }
    },
    populate(id){// here we will populate the table to show the courses to clear a particular selected skill
      this.selected_skill_id = id
      url = "http://localhost:5000/skill/" + id
      axios
          .get(url)
          .then((response) => {
            // handle success
            console.log(response.data.data);
            console.log(response.data.data.linked_courses)
            this.courses_list = response.data.data.linked_courses
          })
          .catch(function (error) {
            // handle error
            console.log(error);
          });

    },
    save(cid,cname){//here we will save the user selection 
      console.log("hello")
      //first grab the current skillid
      let skillid = this.selected_skill_id

      let course_skill = {skillID:skillid, courseName:cname, courseID:cid};

      this.skill_courses_list.push(course_skill)

      console.log(course_skill)
      console.log(this.skill_courses_list[0])

    },
    createlj(){
      console.log("HI");
      console.log(this.skill_courses_list);

      let course_list = [];

      for(let courseobject of this.skill_courses_list) {
        console.log(courseobject);
        course_list.push(courseobject["courseID"]);
      }

      console.log(course_list);

      
      axios
          .post(url, {
            skill_name: this.skillName,
            skill_desc: this.skillDesc,
          })
          .then((response) => {
            // process response.data
            console.log("create response:" + response.data.code);
            
      url = "http://localhost:5000/learningjourney"
      console.log(staff_id);
      axios
          .post(url, {
            staff_id: staff_id,
            lj_name: "test",
            jobrole_id:this.jobrole_id,
            courses : course_list
            })
            .then((response) => {
              console.log("WHY")
            })

    }
  },
  created() {
    this.current_staff_id = staff_id;
    // lets get all the staffs! for the selecting staff_id dropdown :)
    axios.get("http://localhost:5000/staff").then((response) => {
      this.staffs = response.data.data.staffs;
      console.log(this.staffs);
    });

    url = `http://localhost:5000/staff/learningjourney/${staff_id}`;

    axios
      .get(url)
      .then((response) => {
        // process response.data object
        console.log(response.data);
        if (response.data.code == 200) {
          this.learningjourneys = response.data.data.learningjourneys;
          console.log(this.learningjourneys);
          this.lj_name = response.data.data.lj_name;
          this.lj_id = response.data.data.lj_id;
        }
      })
      .catch((error) => {
        // process error object
        console.log(error.response.status);
        //When jobroles database is empty
        if (error.response.status == 404) {
          this.message =
            "<p> There is currently no learning journey created </p>";
        }
      });
  },
});
// (2) Link (mount) Vue instance to DOM
const vm = app1.mount("#app");
