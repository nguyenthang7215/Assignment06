# Experimental Evaluation

| Query | Mode | Expected Top-1 | Actual Top-1 | Success |
|---|---|---|---|---|
| black running shoes | Text | Nike Black Running Shoes | Nike Black Running Shoes | Yes |
| running shoes under 110 dollars | Text | Adidas White Running Shoes | Adidas White Running Shoes | Yes |
| find blue sports shoes | Voice | Blue Sports Shoes | Blue Sports Shoes | Yes |
| find black headphones | Voice | Black Wireless Headphones | Black Wireless Headphones | Yes |
| black_leather_bag.png | Image | Black Leather Bag | Black Leather Bag | Yes |
| green_sports_watch.png | Image | Green Sports Watch | Green Sports Watch | Yes |
| black shoes + sample image | Multimodal | Nike Black Running Shoes | Nike Black Running Shoes | Yes |
| nike shoes under 100 dollars | Text | No result | No result | Yes |
| black shoe | Text | Nike Black Running Shoes | Nike Black Running Shoes | Yes |
| order O001 | Order | O001 | O001 | Yes |

- Total queries: **10**
- Successful queries: **10**
- Success rate: **100.00%**
- Incorrect examples: **None in this controlled test set.**

> This is a small, controlled prototype dataset. The result does not imply production-level accuracy.