import axiosInstance from './index'

const axios = axiosInstance

export const computeFrequentSet = (disThreshold, spatialPrev, temporalPrev, csvFile, csvFileName) => { 
    console.log(csvFile)
    return axios.post(`http://localhost:8000/api/pncop/`, { 'disThreshold': disThreshold, 'spatialPrev': spatialPrev, 'temporalPrev': temporalPrev, 'csvFile': csvFile, 'csvFileName': csvFileName}) 
}