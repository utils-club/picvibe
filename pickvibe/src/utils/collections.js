export const contained_in = function (value, list){
    for (const extension of list) {
      if (value.endsWith(`.${extension}`)) {
        return true
      }
    }
    return false
  }