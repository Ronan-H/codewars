
def find_outlier(nums):
    if (nums[0] ^ nums[1]) % 2 == 1:
        if (nums[1] ^ nums[2]) % 2 == 1:
            return nums[1]
        else:
            return nums[0]

    for n in range(2, len(nums)):
        if (nums[n] ^ nums[n - 1]) % 2 == 1:
            return nums[n]
