# Huffman Compression

Python Implementation of Huffman-Coding for a college project.
You can compress and decompress folders and binary files using this implementation.

* Usage
  ```bash
  # python main.py [input file] -m [compress/decompress]
  Example: python main.py text.txt -m compress
  ```
  
## File Header Format
Number of  Bytes | Description 
--- | --- 
4 | Number of files in the archive
---|**The following header is repeated for each file**
4 | J: Number of bytes to read for the next file
---|**The following bytes has total length of J**
1 | Extra bits appened at the end of the file
4 | N: Length of the encoded Huffman-Tree
N | Encoded Huffman-Tree
4 | File Name (Including parent folder, if compressing a folder.)
4 | K: Length of the encoded file data
K | Encoded file data

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
