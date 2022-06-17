import axios from 'axios'
export const guard = (to, from, next) => {

    const endpoint = 'http://127.0.0.1:5000/guard'
    axios.get(endpoint)
        .then(response => {
            if(response.auth == 1) {
                return next()
            } else {
                const logpoint = 'http://127.0.0.1:5000/login'
                axios.post(logpoint, {
                    nxt:next,
                    ticket:"",
                })
            }
        })

};
