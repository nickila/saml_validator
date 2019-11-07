import axios from "axios";

export default {
    postData: function (formdata) {
        return axios.post("/upload", formdata)
            .then(function (response) {
                console.log(response);
                return response
            })
    }
}
